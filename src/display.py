"""HTTP/WebSocket server + scratchpad overlay.

Serves a browser overlay showing:
- Live scratchpad (mutable, updated in-place)
- Transcript ticker at bottom
- Status indicator
"""

import asyncio
import json
from aiohttp import web

# All connected WebSocket clients
_clients: set = set()

# Event loop reference for thread-safe calls
_loop = None

# Current settings (updated by client dropdowns)
_settings: dict = {"model": "claude-sonnet-4-6", "effort": "medium"}
_stt_settings: dict = {"stt_model": "small"}

# External callback for STT model changes
_on_stt_change = None

# External callback for settings changes
_on_settings_change = None


OVERLAY_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Interview Helper</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Inter', -apple-system, sans-serif;
    background:
        radial-gradient(circle at top, rgba(99, 102, 241, 0.16), transparent 36%),
        #0a0a0f;
    color: #e2e8f0;
    min-height: 100vh;
    overflow-x: hidden;
}

.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
    padding: 12px 20px;
    background: rgba(10, 10, 15, 0.86);
    backdrop-filter: blur(18px);
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    position: sticky;
    top: 0;
    z-index: 100;
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo {
    font-size: 16px;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.mic-indicator {
    display: flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 11px;
    font-weight: 500;
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.mic-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #ef4444;
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.3; }
}

.status-text {
    font-size: 11px;
    color: #64748b;
    white-space: nowrap;
}

.status-text.updating {
    color: #f59e0b;
}

.controls {
    display: flex;
    align-items: center;
    flex-wrap: wrap;
    gap: 10px;
}

.control-group {
    display: flex;
    align-items: center;
    gap: 4px;
}

.control-group label {
    font-size: 10px;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    font-weight: 500;
}

.control-group select {
    background: rgba(30, 30, 50, 0.8);
    color: #e2e8f0;
    border: 1px solid rgba(99, 102, 241, 0.3);
    border-radius: 6px;
    padding: 3px 8px;
    font-size: 12px;
    font-family: 'Inter', sans-serif;
    cursor: pointer;
    outline: none;
    transition: border-color 0.2s;
}

.control-group select:hover {
    border-color: rgba(99, 102, 241, 0.6);
}

.control-group select:focus {
    border-color: #6366f1;
}

.scratchpad {
    padding: 22px 20px 120px;
    max-width: 1120px;
    margin: 0 auto;
    min-height: calc(100vh - 110px);
}

.pad-content {
    display: grid;
    gap: 14px;
    transition: opacity 0.15s ease;
}

.pad-content.updating {
    opacity: 0.74;
}

.lead-card,
.point-card {
    border: 1px solid rgba(99, 102, 241, 0.18);
    background: rgba(15, 23, 42, 0.72);
    box-shadow: 0 14px 40px rgba(0, 0, 0, 0.28);
    transition: transform 0.2s ease, border-color 0.2s ease, background 0.2s ease;
}

.lead-card {
    padding: 18px 20px;
    border-radius: 18px;
    background:
        linear-gradient(135deg, rgba(99, 102, 241, 0.22), rgba(17, 24, 39, 0.92)),
        rgba(15, 23, 42, 0.82);
}

.lead-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 10px;
    border-radius: 999px;
    background: rgba(15, 23, 42, 0.52);
    color: #f8fafc;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.lead-text {
    margin-top: 12px;
    font-size: clamp(26px, 4vw, 40px);
    line-height: 1.16;
    font-weight: 700;
    color: #f8fafc;
    text-wrap: balance;
}

.lead-subpoints {
    margin-top: 12px;
    display: grid;
    gap: 8px;
}

.point-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 12px;
}

.point-card {
    padding: 16px;
    border-radius: 16px;
}

.point-card.flash,
.lead-card.flash {
    border-color: rgba(129, 140, 248, 0.9);
    background-color: rgba(30, 41, 59, 0.92);
    transform: translateY(-1px);
}

.point-label {
    display: inline-flex;
    align-items: center;
    padding: 5px 9px;
    border-radius: 999px;
    background: rgba(99, 102, 241, 0.15);
    color: #c7d2fe;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.03em;
}

.point-body {
    margin-top: 10px;
    font-size: 22px;
    line-height: 1.28;
    color: #f8fafc;
    font-weight: 520;
}

.subpoint {
    margin-top: 8px;
    padding: 10px 12px;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.66);
    font-size: 15px;
    line-height: 1.45;
    color: #cbd5e1;
}

.subpoint::before {
    content: "→";
    margin-right: 8px;
    color: #818cf8;
    font-weight: 700;
}

.empty-state {
    text-align: center;
    padding: 100px 24px;
    color: #475569;
}

.empty-state .icon {
    font-size: 40px;
    margin-bottom: 12px;
    opacity: 0.4;
}

.empty-state p {
    font-size: 14px;
}

.transcript-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    padding: 24px 20px 14px;
    background: linear-gradient(180deg, rgba(10, 10, 15, 0) 0%, rgba(10, 10, 15, 0.97) 30%);
}

.transcript-text {
    max-width: 1120px;
    margin: 0 auto;
    padding: 10px 14px;
    border-radius: 12px;
    background: rgba(15, 23, 42, 0.7);
    border: 1px solid rgba(71, 85, 105, 0.25);
    font-size: 12px;
    line-height: 1.5;
    color: #94a3b8;
    max-height: 58px;
    overflow: hidden;
    font-family: 'JetBrains Mono', monospace;
}

strong {
    color: #ffffff;
    font-weight: 800;
}

.katex {
    font-size: 1.02em;
}

@media (max-width: 720px) {
    .header {
        align-items: flex-start;
    }

    .controls {
        justify-content: flex-end;
    }

    .scratchpad {
        padding-left: 14px;
        padding-right: 14px;
    }

    .point-grid {
        grid-template-columns: 1fr;
    }

    .point-body {
        font-size: 18px;
    }
}
</style>
</head>
<body>

<div class="header">
    <div class="header-left">
        <span class="logo">⚡ Interview Helper</span>
        <div class="mic-indicator">
            <span class="mic-dot"></span>
            <span>LIVE</span>
        </div>
    </div>
    <div class="controls">
        <div class="control-group">
            <label>STT</label>
            <select id="sttSelect">
                <option value="tiny">Tiny</option>
                <option value="base">Base</option>
                <option value="small" selected>Small</option>
                <option value="medium">Medium</option>
                <option value="large-v2">Large</option>
            </select>
        </div>
        <div class="control-group">
            <label>Model</label>
            <select id="modelSelect">
                <optgroup label="Claude">
                    <option value="claude-sonnet-4-6">Sonnet 4.6</option>
                    <option value="claude-opus-4-6">Opus 4.6</option>
                    <option value="claude-haiku-4-5-20251001">Haiku 4.5</option>
                </optgroup>
                <optgroup label="Gemini">
                    <option value="gemini-3.1-flash-lite-preview">Gemini 3.1 Flash Lite</option>
                    <option value="gemini-3-flash-preview">Gemini 3 Flash</option>
                    <option value="gemini-3.1-pro-preview">Gemini 3.1 Pro</option>
                </optgroup>
            </select>
        </div>
        <div class="control-group">
            <label>Effort</label>
            <select id="effortSelect">
                <option value="low">Low</option>
                <option value="medium" selected>Medium</option>
                <option value="high">High</option>
            </select>
        </div>
        <span class="status-text" id="statusText">Connected</span>
    </div>
</div>

<div class="scratchpad">
    <div id="emptyState" class="empty-state">
        <div class="icon">🎤</div>
        <p>Listening... scratchpad will update as conversation flows</p>
    </div>
    <div class="pad-content" id="padContent"></div>
</div>

<div class="transcript-bar">
    <div class="transcript-text" id="transcriptText"></div>
</div>

<script>
const ws = new WebSocket(`ws://${location.host}/ws`);

const padContent = document.getElementById('padContent');
const emptyState = document.getElementById('emptyState');
const transcriptText = document.getElementById('transcriptText');
const statusText = document.getElementById('statusText');
const modelSelect = document.getElementById('modelSelect');
const effortSelect = document.getElementById('effortSelect');
const sttSelect = document.getElementById('sttSelect');

let previousLines = [];

const effortGroup = effortSelect.parentElement;

function sendSettings() {
    ws.send(JSON.stringify({type: 'settings', model: modelSelect.value, effort: effortSelect.value}));
}

function updateEffortVisibility() {
    const isGemini = modelSelect.value.startsWith('gemini');
    effortGroup.style.display = isGemini ? 'none' : 'flex';
}

modelSelect.addEventListener('change', () => { updateEffortVisibility(); sendSettings(); });
effortSelect.addEventListener('change', sendSettings);
sttSelect.addEventListener('change', () => {
    ws.send(JSON.stringify({type: 'stt_settings', stt_model: sttSelect.value}));
});
updateEffortVisibility();

ws.onopen = () => {
    statusText.textContent = 'Connected';
    statusText.style.color = '#10b981';
    statusText.className = 'status-text';
};

ws.onclose = () => {
    statusText.textContent = 'Disconnected';
    statusText.style.color = '#ef4444';
    setTimeout(() => location.reload(), 3000);
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    switch (msg.type) {
        case 'scratchpad':
            emptyState.style.display = 'none';
            statusText.textContent = 'Updated';
            statusText.style.color = '#10b981';
            statusText.className = 'status-text';
            padContent.classList.remove('updating');
            renderScratchpad(msg.text);
            break;

        case 'updating':
            statusText.textContent = '⏳ Thinking...';
            statusText.className = 'status-text updating';
            padContent.classList.add('updating');
            break;

        case 'transcript':
            transcriptText.textContent = msg.text;
            break;

        case 'error':
            statusText.textContent = '⚠️ ' + msg.text;
            statusText.style.color = '#ef4444';
            padContent.classList.remove('updating');
            break;
    }
};

function renderScratchpad(text) {
    const items = parseScratchpad(text);
    const signatures = items.map(item => `${item.raw}||${item.subpoints.join('||')}`);
    const lead = items.length && items[0].raw.startsWith('⚡') ? items.shift() : null;
    let signatureIndex = 0;
    const parts = [];

    if (lead) {
        const leadSig = signatures[signatureIndex++];
        const isNewLead = previousLines[0] !== leadSig;
        parts.push(renderLeadCard(lead, isNewLead));
    }

    if (items.length) {
        const cards = items.map(item => {
            const sig = signatures[signatureIndex];
            const isNew = previousLines[signatureIndex] !== sig;
            signatureIndex += 1;
            return renderPointCard(item, isNew);
        }).join('');
        parts.push(`<div class="point-grid">${cards}</div>`);
    }

    padContent.innerHTML = parts.join('');
    previousLines = signatures;

    if (typeof renderMathInElement === 'function') {
        renderMathInElement(padContent, {
            delimiters: [
                {left: '$$', right: '$$', display: true},
                {left: '$', right: '$', display: false},
                {left: '\\\\(', right: '\\\\)', display: false},
                {left: '\\\\[', right: '\\\\]', display: true},
            ],
            throwOnError: false,
        });
    }

    setTimeout(() => {
        document.querySelectorAll('.flash').forEach(el => {
            el.classList.remove('flash');
        });
    }, 1500);
}

function parseScratchpad(text) {
    const items = [];
    let current = null;

    text.split('\\n').forEach(rawLine => {
        if (!rawLine.trim()) return;

        const isSubpoint = rawLine.startsWith('  ') || rawLine.startsWith('\\t');
        const trimmed = rawLine.trim();

        if (isSubpoint || trimmed.startsWith('→')) {
            if (current) {
                current.subpoints.push(trimmed.replace(/^→\\s*/, ''));
            }
            return;
        }

        current = {raw: trimmed, subpoints: []};
        items.push(current);
    });

    return items;
}

function renderLeadCard(item, isNew) {
    const {label, body} = splitLabel(stripMarker(item.raw));
    const eyebrow = label || 'Say next';
    const leadText = body || stripMarker(item.raw);
    const subpoints = item.subpoints.length
        ? `<div class="lead-subpoints">${item.subpoints.map(renderSubpoint).join('')}</div>`
        : '';

    return `
        <section class="lead-card${isNew ? ' flash' : ''}">
            <div class="lead-eyebrow">⚡ ${renderInline(eyebrow)}</div>
            <div class="lead-text">${renderInline(leadText)}</div>
            ${subpoints}
        </section>
    `;
}

function renderPointCard(item, isNew) {
    const stripped = stripMarker(item.raw);
    const {label, body} = splitLabel(stripped);
    const cardBody = body || stripped;
    const chip = label ? `<div class="point-label">${renderInline(label)}</div>` : '';
    const subpoints = item.subpoints.map(renderSubpoint).join('');

    return `
        <article class="point-card${isNew ? ' flash' : ''}">
            ${chip}
            <div class="point-body">${renderInline(cardBody)}</div>
            ${subpoints}
        </article>
    `;
}

function renderSubpoint(text) {
    return `<div class="subpoint">${renderInline(text)}</div>`;
}

function splitLabel(text) {
    const match = text.match(/^([^:]{1,24}):\\s*(.+)$/);
    if (!match) return {label: '', body: text};
    return {label: match[1].trim(), body: match[2].trim()};
}

function stripMarker(text) {
    return text.replace(/^⚡\\s*/, '').replace(/^•\\s*/, '').trim();
}

function renderInline(text) {
    return escapeHtml(text).replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
</script>
</body>
</html>"""


async def _websocket_handler(request):
    """Handle WebSocket connections."""
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    _clients.add(ws)
    print(f"[Display] Client connected ({len(_clients)} total)")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    if data.get("type") == "settings":
                        _settings["model"] = data.get("model", _settings["model"])
                        _settings["effort"] = data.get("effort", _settings["effort"])
                        print(f"[Display] Settings updated: model={_settings['model']}, effort={_settings['effort']}")
                        if _on_settings_change:
                            _on_settings_change(_settings.copy())
                    elif data.get("type") == "stt_settings":
                        new_stt = data.get("stt_model", _stt_settings["stt_model"])
                        if new_stt != _stt_settings["stt_model"]:
                            _stt_settings["stt_model"] = new_stt
                            print(f"[Display] STT model updated: {new_stt}")
                            if _on_stt_change:
                                _on_stt_change(new_stt)
                except json.JSONDecodeError:
                    pass
    finally:
        _clients.discard(ws)
        print(f"[Display] Client disconnected ({len(_clients)} total)")

    return ws


async def _index_handler(request):
    """Serve the overlay HTML page."""
    return web.Response(text=OVERLAY_HTML, content_type="text/html")


async def broadcast(data: dict):
    """Send a message to all connected WebSocket clients."""
    if not _clients:
        return

    msg = json.dumps(data)
    dead = set()
    for ws in _clients:
        try:
            await ws.send_str(msg)
        except Exception:
            dead.add(ws)
    _clients.difference_update(dead)


def broadcast_threadsafe(data: dict):
    """Thread-safe broadcast — call from non-async code."""
    if _loop and _loop.is_running():
        asyncio.run_coroutine_threadsafe(broadcast(data), _loop)


def send_scratchpad(text: str):
    """Send the full updated scratchpad to all clients."""
    broadcast_threadsafe({"type": "scratchpad", "text": text})


def send_updating():
    """Notify clients that an update is in progress."""
    broadcast_threadsafe({"type": "updating"})


def send_transcript(text: str):
    """Update the transcript ticker."""
    broadcast_threadsafe({"type": "transcript", "text": text})


def send_error(text: str):
    """Send error to clients."""
    broadcast_threadsafe({"type": "error", "text": text})


def get_settings() -> dict:
    """Return current model/effort settings."""
    return _settings.copy()


def set_on_settings_change(callback):
    """Register a callback for when the user changes settings."""
    global _on_settings_change
    _on_settings_change = callback


def set_on_stt_change(callback):
    """Register a callback for when the user changes the STT model."""
    global _on_stt_change
    _on_stt_change = callback


def reset():
    """Reset module state — useful between tests."""
    global _loop, _on_settings_change, _on_stt_change
    _clients.clear()
    _loop = None
    _on_settings_change = None
    _on_stt_change = None
    _settings.update({"model": "claude-sonnet-4-6", "effort": "medium"})
    _stt_settings.update({"stt_model": "small"})


async def start_server(host: str = "0.0.0.0", port: int = 8888):
    """Start the aiohttp server."""
    global _loop
    _clients.clear()
    _loop = asyncio.get_event_loop()

    app = web.Application()
    app.router.add_get("/", _index_handler)
    app.router.add_get("/ws", _websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, host, port)
    await site.start()
    print(f"[Display] Server running at http://localhost:{port}")
    return runner

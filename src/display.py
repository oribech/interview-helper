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
    background: #0a0a0f;
    color: #e2e8f0;
    min-height: 100vh;
    overflow-x: hidden;
}

/* Header */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 10px 20px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
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
}

.status-text.updating {
    color: #f59e0b;
}

/* Dropdowns */
.controls {
    display: flex;
    align-items: center;
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

/* Scratchpad */
.scratchpad {
    padding: 24px 28px;
    max-width: 800px;
    margin: 0 auto;
    min-height: calc(100vh - 120px);
}

.pad-content {
    font-size: 16px;
    line-height: 2;
    color: #e2e8f0;
    letter-spacing: 0.01em;
    transition: opacity 0.15s ease;
}

.pad-content.updating {
    opacity: 0.7;
}

/* Bullet styling */
.pad-content .line {
    padding: 4px 0;
    border-bottom: 1px solid rgba(51, 65, 85, 0.15);
    transition: all 0.2s ease;
}

.pad-content .line:last-child {
    border-bottom: none;
}

.pad-content .line.flash {
    background: rgba(99, 102, 241, 0.08);
    border-radius: 6px;
    padding-left: 8px;
    margin-left: -8px;
}

.pad-content .line.sub {
    padding-left: 24px;
    font-size: 14px;
    color: #94a3b8;
    border-bottom: none;
    line-height: 1.8;
}

/* Empty state */
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

/* Transcript ticker */
.transcript-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, rgba(10, 10, 15, 0) 0%, rgba(10, 10, 15, 0.95) 30%);
    padding: 28px 20px 12px;
}

.transcript-text {
    font-size: 12px;
    color: #475569;
    font-style: italic;
    max-height: 36px;
    overflow: hidden;
    font-family: 'JetBrains Mono', monospace;
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
            <label>Model</label>
            <select id="modelSelect">
                <option value="claude-sonnet-4-6">Sonnet 4.6</option>
                <option value="claude-opus-4-6">Opus 4.6</option>
                <option value="claude-haiku-4-5-20251001">Haiku 4.5</option>
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

let previousLines = [];

// Send settings changes to server
modelSelect.addEventListener('change', () => {
    ws.send(JSON.stringify({type: 'settings', model: modelSelect.value, effort: effortSelect.value}));
});
effortSelect.addEventListener('change', () => {
    ws.send(JSON.stringify({type: 'settings', model: modelSelect.value, effort: effortSelect.value}));
});

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
    const lines = text.split('\\n').filter(l => l.trim());
    const newHtml = lines.map((line, i) => {
        const isSub = line.startsWith('  ');
        const cleaned = escapeHtml(line.trim());

        // Bold markdown
        const rendered = cleaned.replace(/\\*\\*(.+?)\\*\\*/g, '<strong>$1</strong>');

        const cls = isSub ? 'line sub' : 'line';

        // Flash if this line is new or changed
        const isNew = !previousLines[i] || previousLines[i] !== line;
        const flashCls = isNew ? ' flash' : '';

        return `<div class="${cls}${flashCls}">${rendered}</div>`;
    }).join('');

    padContent.innerHTML = newHtml;
    previousLines = lines;

    // Render LaTeX formulas
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

    // Remove flash after animation
    setTimeout(() => {
        document.querySelectorAll('.line.flash').forEach(el => {
            el.classList.remove('flash');
        });
    }, 1500);
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


def reset():
    """Reset module state — useful between tests."""
    global _loop, _on_settings_change
    _clients.clear()
    _loop = None
    _on_settings_change = None
    _settings.update({"model": "claude-sonnet-4-6", "effort": "medium"})


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

"""HTTP/WebSocket server + overlay HTML.

Serves a browser overlay that displays:
- Live mic indicator
- Detected question
- Streamed answer from Claude
- Transcript ticker at bottom
"""

import asyncio
import json
from aiohttp import web

# All connected WebSocket clients
_clients: set = set()

# Event loop reference for thread-safe calls
_loop: asyncio.AbstractEventLoop = None


OVERLAY_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Interview Helper</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
    font-family: 'Inter', -apple-system, sans-serif;
    background: #0a0a0f;
    color: #e2e8f0;
    min-height: 100vh;
    overflow-x: hidden;
}

/* Header bar */
.header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 12px 24px;
    background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
    border-bottom: 1px solid rgba(99, 102, 241, 0.2);
    position: sticky;
    top: 0;
    z-index: 100;
    backdrop-filter: blur(10px);
}

.header-left {
    display: flex;
    align-items: center;
    gap: 12px;
}

.logo {
    font-size: 18px;
    font-weight: 700;
    background: linear-gradient(135deg, #818cf8, #6366f1);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -0.5px;
}

.mic-indicator {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 500;
    transition: all 0.3s;
}

.mic-indicator.listening {
    background: rgba(239, 68, 68, 0.15);
    color: #ef4444;
    border: 1px solid rgba(239, 68, 68, 0.3);
}

.mic-indicator.idle {
    background: rgba(100, 116, 139, 0.15);
    color: #94a3b8;
    border: 1px solid rgba(100, 116, 139, 0.3);
}

.mic-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
}

.mic-indicator.listening .mic-dot {
    animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(1.3); }
}

.status-text {
    font-size: 12px;
    color: #64748b;
}

/* Main content */
.main {
    padding: 24px;
    max-width: 900px;
    margin: 0 auto;
}

/* Question card */
.question-card {
    background: linear-gradient(135deg, rgba(99, 102, 241, 0.08) 0%, rgba(139, 92, 246, 0.08) 100%);
    border: 1px solid rgba(99, 102, 241, 0.2);
    border-radius: 16px;
    padding: 20px 24px;
    margin-bottom: 20px;
    display: none;
    animation: slideIn 0.3s ease-out;
}

.question-card.visible {
    display: block;
}

@keyframes slideIn {
    from { opacity: 0; transform: translateY(-10px); }
    to { opacity: 1; transform: translateY(0); }
}

.question-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #818cf8;
    font-weight: 600;
    margin-bottom: 8px;
}

.question-text {
    font-size: 16px;
    font-weight: 500;
    color: #f1f5f9;
    line-height: 1.5;
}

/* Answer area */
.answer-card {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(51, 65, 85, 0.5);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 20px;
    min-height: 120px;
    display: none;
    animation: fadeIn 0.4s ease-out;
}

.answer-card.visible {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.answer-label {
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #10b981;
    font-weight: 600;
    margin-bottom: 12px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.answer-label .spinner {
    width: 12px;
    height: 12px;
    border: 2px solid rgba(16, 185, 129, 0.3);
    border-top-color: #10b981;
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
    display: none;
}

.answer-label .spinner.active {
    display: inline-block;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.answer-text {
    font-size: 14px;
    line-height: 1.7;
    color: #cbd5e1;
    white-space: pre-wrap;
}

.answer-text strong {
    color: #f1f5f9;
    font-weight: 600;
}

.answer-text code {
    background: rgba(99, 102, 241, 0.15);
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 13px;
    color: #a5b4fc;
}

/* Transcript ticker */
.transcript-bar {
    position: fixed;
    bottom: 0;
    left: 0;
    right: 0;
    background: linear-gradient(180deg, rgba(10, 10, 15, 0) 0%, rgba(10, 10, 15, 0.95) 30%);
    padding: 32px 24px 16px;
}

.transcript-label {
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    color: #475569;
    font-weight: 600;
    margin-bottom: 6px;
}

.transcript-text {
    font-size: 13px;
    color: #64748b;
    line-height: 1.5;
    max-height: 40px;
    overflow: hidden;
    font-style: italic;
}

/* Empty state */
.empty-state {
    text-align: center;
    padding: 80px 24px;
    color: #475569;
}

.empty-state .icon {
    font-size: 48px;
    margin-bottom: 16px;
    opacity: 0.5;
}

.empty-state h2 {
    font-size: 18px;
    font-weight: 500;
    color: #64748b;
    margin-bottom: 8px;
}

.empty-state p {
    font-size: 14px;
    color: #475569;
}

/* History */
.history {
    margin-top: 24px;
    border-top: 1px solid rgba(51, 65, 85, 0.3);
    padding-top: 20px;
}

.history-item {
    background: rgba(15, 23, 42, 0.3);
    border: 1px solid rgba(51, 65, 85, 0.3);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    opacity: 0.6;
    transition: opacity 0.2s;
}

.history-item:hover {
    opacity: 1;
}

.history-item .q {
    font-size: 13px;
    color: #818cf8;
    font-weight: 500;
    margin-bottom: 6px;
}

.history-item .a {
    font-size: 12px;
    color: #94a3b8;
    line-height: 1.5;
    white-space: pre-wrap;
}
</style>
</head>
<body>

<div class="header">
    <div class="header-left">
        <span class="logo">⚡ Interview Helper</span>
        <div id="micIndicator" class="mic-indicator listening">
            <span class="mic-dot"></span>
            <span>LISTENING</span>
        </div>
    </div>
    <span class="status-text" id="statusText">Connected</span>
</div>

<div class="main">
    <div id="emptyState" class="empty-state">
        <div class="icon">🎤</div>
        <h2>Listening for questions...</h2>
        <p>Speak naturally — questions will be detected automatically</p>
    </div>

    <div id="questionCard" class="question-card">
        <div class="question-label">Detected Question</div>
        <div class="question-text" id="questionText"></div>
    </div>

    <div id="answerCard" class="answer-card">
        <div class="answer-label">
            <span>Claude's Answer</span>
            <span class="spinner" id="spinner"></span>
        </div>
        <div class="answer-text" id="answerText"></div>
    </div>

    <div id="history" class="history" style="display:none;"></div>
</div>

<div class="transcript-bar">
    <div class="transcript-label">Live Transcript</div>
    <div class="transcript-text" id="transcriptText">Waiting for speech...</div>
</div>

<script>
const ws = new WebSocket(`ws://${location.host}/ws`);

const questionCard = document.getElementById('questionCard');
const questionText = document.getElementById('questionText');
const answerCard = document.getElementById('answerCard');
const answerText = document.getElementById('answerText');
const transcriptText = document.getElementById('transcriptText');
const emptyState = document.getElementById('emptyState');
const spinner = document.getElementById('spinner');
const statusText = document.getElementById('statusText');
const history = document.getElementById('history');

let currentAnswer = '';
let qaHistory = [];

ws.onopen = () => {
    statusText.textContent = 'Connected';
    statusText.style.color = '#10b981';
};

ws.onclose = () => {
    statusText.textContent = 'Disconnected';
    statusText.style.color = '#ef4444';
    setTimeout(() => location.reload(), 3000);
};

ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);

    switch (msg.type) {
        case 'question':
            emptyState.style.display = 'none';
            questionCard.classList.add('visible');
            answerCard.classList.add('visible');
            questionText.textContent = msg.text;
            answerText.textContent = '';
            currentAnswer = '';
            spinner.classList.add('active');
            break;

        case 'answer_chunk':
            currentAnswer += msg.text;
            answerText.textContent = currentAnswer;
            // Auto-scroll
            answerCard.scrollTop = answerCard.scrollHeight;
            break;

        case 'answer_done':
            spinner.classList.remove('active');
            // Save to history
            if (questionText.textContent && currentAnswer) {
                qaHistory.unshift({
                    q: questionText.textContent,
                    a: currentAnswer,
                });
                renderHistory();
            }
            break;

        case 'transcript':
            transcriptText.textContent = msg.text;
            break;

        case 'status':
            statusText.textContent = msg.text;
            break;
    }
};

function renderHistory() {
    if (qaHistory.length <= 1) return;
    history.style.display = 'block';
    // Show all except current (index 0)
    history.innerHTML = qaHistory.slice(1, 6).map(item =>
        `<div class="history-item">
            <div class="q">Q: ${escapeHtml(item.q)}</div>
            <div class="a">${escapeHtml(item.a)}</div>
        </div>`
    ).join('');
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
            pass  # We only push, don't receive
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
    # Use difference_update to mutate in-place (avoids rebinding _clients)
    _clients.difference_update(dead)


def broadcast_threadsafe(data: dict):
    """Thread-safe broadcast — call from non-async code."""
    if _loop and _loop.is_running():
        asyncio.run_coroutine_threadsafe(broadcast(data), _loop)


def send_question(text: str):
    """Notify all clients that a question was detected."""
    broadcast_threadsafe({"type": "question", "text": text})


def send_answer_chunk(text: str):
    """Stream an answer chunk to all clients."""
    broadcast_threadsafe({"type": "answer_chunk", "text": text})


def send_answer_done():
    """Notify clients that the answer is complete."""
    broadcast_threadsafe({"type": "answer_done"})


def send_transcript(text: str):
    """Update the transcript ticker."""
    broadcast_threadsafe({"type": "transcript", "text": text})


def send_status(text: str):
    """Update the status text."""
    broadcast_threadsafe({"type": "status", "text": text})


def reset():
    """Reset module state — useful between tests."""
    global _loop
    _clients.clear()
    _loop = None


async def start_server(host: str = "0.0.0.0", port: int = 8888):
    """Start the aiohttp server. Call from the main event loop."""
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

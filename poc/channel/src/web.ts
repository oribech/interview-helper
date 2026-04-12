import type { ScratchpadState, TraceEvent } from './state.js'

function sseChunk(event: string, data: unknown) {
  return `event: ${event}\ndata: ${JSON.stringify(data)}\n\n`
}

export class WebState {
  private listeners = new Set<(chunk: string) => void>()

  subscribe(emit: (chunk: string) => void) {
    this.listeners.add(emit)
    return () => this.listeners.delete(emit)
  }

  publishState(state: ScratchpadState) {
    const chunk = sseChunk('scratchpad', state)
    for (const emit of this.listeners) emit(chunk)
  }

  publishTrace(event: TraceEvent) {
    const chunk = sseChunk('trace', event)
    for (const emit of this.listeners) emit(chunk)
  }
}

export function renderIndexHtml(initialState: ScratchpadState) {
  const initialJson = JSON.stringify(initialState).replace(/</g, '\\u003c')
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Interview Scratchpad</title>
  <style>
    :root { color-scheme: dark; }
    body { margin: 0; font-family: Inter, ui-sans-serif, system-ui, sans-serif; background: #0b1020; color: #eef2ff; }
    .page { max-width: 960px; margin: 0 auto; padding: 24px; }
    .header { display:flex; justify-content:space-between; align-items:center; margin-bottom:16px; }
    .pill { padding: 6px 10px; border-radius:999px; background:#1e293b; color:#cbd5e1; font-size:12px; border:1px solid #334155; }
    .pill.listening { color:#cbd5e1; }
    .pill.draft { color:#fbbf24; }
    .pill.refined, .pill.final { color:#86efac; }
    .pill.stale { color:#fca5a5; }
    .scratchpad { display:grid; gap:16px; }
    .card { background:#111827; border:1px solid #243146; border-radius:18px; padding:18px; box-shadow:0 12px 40px rgba(0,0,0,.25); }
    .label { color:#93c5fd; font-size:12px; text-transform:uppercase; letter-spacing:.08em; margin-bottom:8px; }
    .question { font-size:24px; font-weight:700; line-height:1.2; }
    .answer { font-size:20px; line-height:1.4; }
    .formula { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; white-space:pre-wrap; font-size:18px; line-height:1.5; color:#fde68a; }
    ul { margin:0; padding-left:20px; }
    li { margin: 0 0 8px; font-size:18px; }
    .muted { color:#94a3b8; font-size:15px; }
    .grid { display:grid; grid-template-columns: 2fr 1fr; gap:16px; }
    .meta { display:flex; gap:10px; flex-wrap:wrap; }
    .meta span { padding:4px 8px; border-radius:999px; background:#172036; color:#cbd5e1; font-size:12px; }
    .trace { margin-top:8px; max-height:280px; overflow:auto; font-family: ui-monospace, monospace; font-size:12px; color:#94a3b8; }
    details.card summary { cursor:pointer; color:#93c5fd; }
    @media (max-width: 860px) { .grid { grid-template-columns: 1fr; } .question { font-size:20px; } .answer, li, .formula { font-size:16px; } }
  </style>
</head>
<body>
  <div class="page">
    <div class="header">
      <h1 style="margin:0; font-size:22px;">Interview Scratchpad</h1>
      <div class="pill" id="status-pill">listening</div>
    </div>
    <div class="scratchpad">
      <div class="card">
        <div class="label">Question</div>
        <div class="question" id="question"></div>
      </div>
      <div class="grid">
        <div class="card">
          <div class="label">Short answer</div>
          <div class="answer" id="short_answer"></div>
        </div>
        <div class="card">
          <div class="label">Confidence</div>
          <div class="answer" id="confidence"></div>
        </div>
      </div>
      <div class="card">
        <div class="label">Formula / structure</div>
        <div class="formula" id="formula_or_structure"></div>
      </div>
      <div class="card">
        <div class="label">Say these</div>
        <ul id="say_bullets"></ul>
      </div>
      <div class="card">
        <div class="label">Caveat</div>
        <div class="muted" id="caveat"></div>
      </div>
      <div class="card">
        <div class="label">Sources</div>
        <div class="meta" id="citations"></div>
      </div>
      <div class="card muted">Updated <span id="updated_at"></span></div>
      <details class="card">
        <summary>Debug trace</summary>
        <div class="trace" id="trace"></div>
      </details>
    </div>
  </div>
  <script>
    const state = ${initialJson};
    const traceEl = document.getElementById('trace');
    function render(next) {
      const pill = document.getElementById('status-pill');
      pill.textContent = next.status + ' · v' + next.version;
      pill.className = 'pill ' + (next.status || 'listening');
      document.getElementById('question').textContent = next.question || 'Listening for the next interviewer turn…';
      document.getElementById('short_answer').textContent = next.short_answer || 'Waiting for a question pause…';
      document.getElementById('formula_or_structure').textContent = next.formula_or_structure || '—';
      document.getElementById('caveat').textContent = next.caveat || '—';
      document.getElementById('confidence').textContent = Math.round((next.confidence || 0) * 100) + '%';
      document.getElementById('updated_at').textContent = next.updated_at || '—';
      const ul = document.getElementById('say_bullets');
      ul.innerHTML = '';
      (next.say_bullets || []).forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        ul.appendChild(li);
      });
      const citations = document.getElementById('citations');
      citations.innerHTML = '';
      (next.citations || []).forEach(item => {
        const el = document.createElement('span');
        el.textContent = item;
        citations.appendChild(el);
      });
      if (!citations.childNodes.length) {
        const el = document.createElement('span');
        el.textContent = 'No sources yet';
        citations.appendChild(el);
      }
    }
    render(state);
    const es = new EventSource('/events');
    es.addEventListener('scratchpad', (evt) => {
      const next = JSON.parse(evt.data);
      render(next);
    });
    es.addEventListener('trace', (evt) => {
      const t = JSON.parse(evt.data);
      const line = document.createElement('div');
      line.textContent = '[' + t.at + '] ' + t.type + ' ' + JSON.stringify(t.payload);
      traceEl.prepend(line);
      while (traceEl.childNodes.length > 50) traceEl.removeChild(traceEl.lastChild);
    });
  </script>
</body>
</html>`
}

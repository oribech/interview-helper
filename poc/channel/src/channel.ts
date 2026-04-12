#!/usr/bin/env bun
import { mkdirSync, appendFileSync } from 'node:fs'
import { dirname, join } from 'node:path'
import { Server } from '@modelcontextprotocol/sdk/server/index.js'
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js'
import { ListToolsRequestSchema, CallToolRequestSchema } from '@modelcontextprotocol/sdk/types.js'
import { z } from 'zod'
import { DEFAULT_CHAT_ID, clampScratchpadPatch, initialState, type TraceEvent, type TranscriptTurn, type RetrievedSnippet } from './state.js'
import { replyToolSchema } from './replyTool.js'
import { WebState, renderIndexHtml } from './web.js'

const projectRoot = process.env.INTERVIEW_PROJECT_ROOT || process.cwd()
const port = Number(process.env.INTERVIEW_CHANNEL_PORT || 8788)
const traceDir = process.env.INTERVIEW_TRACE_DIR || join(projectRoot, 'poc', 'runs')
const retrievalScript = join(projectRoot, 'poc', 'retrieval', 'retrieve.py')
const traceFile = join(traceDir, `trace-${Date.now()}.jsonl`)
mkdirSync(dirname(traceFile), { recursive: true })

const sse = new WebState()
const stateByChat = new Map<string, ReturnType<typeof initialState>>()
stateByChat.set(DEFAULT_CHAT_ID, initialState())

function currentState(chatId = DEFAULT_CHAT_ID) {
  if (!stateByChat.has(chatId)) stateByChat.set(chatId, initialState(chatId))
  return stateByChat.get(chatId)!
}

function broadcastTrace(type: string, payload: unknown) {
  const event: TraceEvent = { type, at: new Date().toISOString(), payload }
  appendFileSync(traceFile, JSON.stringify(event) + '\n')
  sse.publishTrace(event)
}

function publishState(chatId = DEFAULT_CHAT_ID) {
  const state = currentState(chatId)
  appendFileSync(traceFile, JSON.stringify({ type: 'scratchpad_state', at: new Date().toISOString(), payload: state }) + '\n')
  sse.publishState(state)
}

async function retrieveContext(query: string): Promise<RetrievedSnippet[]> {
  const proc = Bun.spawn(['python3', retrievalScript, '--query', query, '--top-k', '4', '--json'], {
    cwd: projectRoot,
    stdout: 'pipe',
    stderr: 'pipe',
  })
  const stdout = await new Response(proc.stdout).text()
  const stderr = await new Response(proc.stderr).text()
  const exitCode = await proc.exited
  if (exitCode !== 0) {
    broadcastTrace('retrieval_error', { query, exitCode, stderr })
    return []
  }
  try {
    const parsed = JSON.parse(stdout)
    return Array.isArray(parsed.results) ? parsed.results : []
  } catch (error) {
    broadcastTrace('retrieval_parse_error', { query, stdout, error: String(error) })
    return []
  }
}

function formatTranscriptTail(turns: TranscriptTurn[]) {
  return turns.slice(-6).map(turn => `- ${turn.speaker}: ${turn.text}`).join('\n')
}

function formatRetrieval(snippets: RetrievedSnippet[]) {
  if (!snippets.length) return 'No retrieved snippets.'
  return snippets.map((item, idx) => `(${idx + 1}) [${item.title}] ${item.snippet}`).join('\n')
}

function pushTurn(chatId: string, turn: TranscriptTurn) {
  const state = currentState(chatId)
  state.transcript_tail = [...state.transcript_tail.slice(-7), turn]
  state.updated_at = new Date().toISOString()
  state.last_event_type = turn.source || 'transcript.final'
  publishState(chatId)
}

const mcp = new Server(
  { name: 'interview_sidecar', version: '0.0.1' },
  {
    capabilities: {
      experimental: {
        'claude/channel': {},
      },
      tools: {},
    },
    instructions:
      'Messages arrive as <channel source="interview_sidecar" chat_id="..." event_type="..." speaker="...">...</channel>. ' +
      'You are updating a live interview scratchpad shown on a second monitor. ' +
      'Always respond by calling the reply tool exactly once. Never answer in plain text. ' +
      'Every channel message contains a Request ID. Echo that exact Request ID in reply.request_id. Older Request IDs are stale and will be ignored. ' +
      'Keep it glanceable: question one line; short_answer max 2 lines; formula_or_structure compact and prominent; say_bullets max 3; caveat max 1 line. ' +
      'Prefer formulas, SQL skeletons, experiment design checklists, and decision frameworks. ' +
      'If the question is incomplete, emit status draft or listening with lower confidence. ' +
      'When a later event changes the answer, replace the old content and mark stale only if the old content is now wrong. ' +
      'For candidate turns, preserve the existing scratchpad unless the candidate clarifies the question. ' +
      'Use citations as short relative source identifiers from the retrieved snippets.',
  },
)

mcp.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: 'reply',
    description: 'Update the web scratchpad for this interview chat.',
    inputSchema: replyToolSchema,
  }],
}))

mcp.setRequestHandler(CallToolRequestSchema, async req => {
  if (req.params.name !== 'reply') throw new Error(`unknown tool: ${req.params.name}`)
  const args = req.params.arguments as Record<string, unknown>
  const chatId = String(args.chat_id ?? DEFAULT_CHAT_ID)
  const state = currentState(chatId)
  const requestId = Number(args.request_id ?? -1)
  if (requestId !== state.pending_request_id) {
    broadcastTrace('stale_reply_ignored', { chatId, requestId, pending_request_id: state.pending_request_id, args })
    return { content: [{ type: 'text', text: 'ignored stale reply' }] }
  }
  const next = clampScratchpadPatch(args, state)
  next.last_event_type = 'reply'
  next.pending_request_id = requestId
  stateByChat.set(chatId, next)
  broadcastTrace('reply_tool', args)
  publishState(chatId)
  return { content: [{ type: 'text', text: 'scratchpad updated' }] }
})

await mcp.connect(new StdioServerTransport())
broadcastTrace('server_started', { port, traceFile })

const IngestSchema = z.object({
  type: z.string(),
  chat_id: z.string().default(DEFAULT_CHAT_ID),
  speaker_guess: z.string().default('unknown'),
  text: z.string().default(''),
  ts: z.string().optional(),
  source: z.string().optional(),
})

Bun.serve({
  port,
  hostname: '127.0.0.1',
  idleTimeout: 0,
  async fetch(req) {
    const url = new URL(req.url)
    if (req.method === 'GET' && url.pathname === '/') {
      return new Response(renderIndexHtml(currentState()), { headers: { 'Content-Type': 'text/html; charset=utf-8' } })
    }
    if (req.method === 'GET' && url.pathname === '/state') {
      return Response.json(currentState())
    }
    if (req.method === 'POST' && url.pathname === '/reset') {
      const body = req.headers.get('content-type')?.includes('application/json') ? await req.json() : {}
      const chatId = String((body as any)?.chat_id ?? DEFAULT_CHAT_ID)
      stateByChat.set(chatId, initialState(chatId))
      broadcastTrace('reset', { chatId })
      publishState(chatId)
      return Response.json({ ok: true, chat_id: chatId })
    }
    if (req.method === 'GET' && url.pathname === '/events') {
      const stream = new ReadableStream({
        start(controller) {
          controller.enqueue(': connected\n\n')
          controller.enqueue(`event: scratchpad\ndata: ${JSON.stringify(currentState())}\n\n`)
          const unsubscribe = sse.subscribe(chunk => controller.enqueue(chunk))
          req.signal.addEventListener('abort', unsubscribe)
        },
      })
      return new Response(stream, {
        headers: {
          'Content-Type': 'text/event-stream',
          'Cache-Control': 'no-cache',
          'Connection': 'keep-alive',
        },
      })
    }
    if (req.method === 'POST' && url.pathname === '/ingest') {
      const payload = IngestSchema.parse(await req.json())
      const chatId = payload.chat_id
      const turn: TranscriptTurn = {
        id: `${Date.now()}-${Math.random().toString(16).slice(2, 8)}`,
        speaker: payload.speaker_guess,
        text: payload.text,
        ts: payload.ts || new Date().toISOString(),
        source: payload.type,
      }
      if (payload.type.startsWith('transcript')) {
        pushTurn(chatId, turn)
        broadcastTrace('transcript_event', payload)
        if (payload.type === 'transcript.partial') {
          const state = currentState(chatId)
          state.status = 'listening'
          state.question = payload.speaker_guess === 'interviewer' ? payload.text.slice(0, 240) : state.question
          state.updated_at = new Date().toISOString()
          publishState(chatId)
        }
        return Response.json({ ok: true, queued: false })
      }
      if (payload.type === 'question.pause' || payload.type === 'question.update') {
        const state = currentState(chatId)
        state.pending_request_id += 1
        const requestId = state.pending_request_id
        state.question = (payload.text || state.question).slice(0, 240)
        state.status = payload.type === 'question.update' ? 'draft' : state.status
        state.updated_at = new Date().toISOString()
        publishState(chatId)
        const transcriptTail = formatTranscriptTail(state.transcript_tail)
        const snippets = await retrieveContext(payload.text || state.question)
        const citations = snippets.map(item => item.source_path).slice(0, 4)
        const content = [
          `Request ID: ${requestId}`,
          `Event: ${payload.type}`,
          `Speaker: ${payload.speaker_guess}`,
          `Current question hypothesis: ${payload.text || state.question || '(none yet)'}`,
          '',
          'Recent transcript:',
          transcriptTail || '(none)',
          '',
          'Current scratchpad:',
          JSON.stringify({
            question: state.question,
            status: state.status,
            short_answer: state.short_answer,
            formula_or_structure: state.formula_or_structure,
            say_bullets: state.say_bullets,
            caveat: state.caveat,
            confidence: state.confidence,
            version: state.version,
          }, null, 2),
          '',
          'Retrieved snippets:',
          formatRetrieval(snippets),
          '',
          `Suggested citations: ${citations.join(', ') || 'none'}`,
          '',
          'Update the scratchpad now.',
        ].join('\n')
        broadcastTrace('channel_notification', { chatId, type: payload.type, content })
        await mcp.notification({
          method: 'notifications/claude/channel',
          params: {
            content,
            meta: {
              chat_id: chatId,
              event_type: payload.type,
              speaker: payload.speaker_guess,
            },
          },
        })
        return Response.json({ ok: true, queued: true, snippets })
      }
      return new Response('unsupported event type', { status: 400 })
    }
    return new Response('not found', { status: 404 })
  },
})

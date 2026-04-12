export type ScratchpadStatus = 'listening' | 'draft' | 'refined' | 'final' | 'stale'

export interface TranscriptTurn {
  id: string
  speaker: string
  text: string
  ts: string
  source?: string
}

export interface RetrievedSnippet {
  source_path: string
  title: string
  snippet: string
  score: number
}

export interface ScratchpadState {
  chat_id: string
  pending_request_id: number
  question: string
  status: ScratchpadStatus
  short_answer: string
  formula_or_structure: string
  say_bullets: string[]
  caveat: string
  confidence: number
  version: number
  citations: string[]
  transcript_tail: TranscriptTurn[]
  last_event_type: string
  updated_at: string
}

export interface TraceEvent {
  type: string
  at: string
  payload: unknown
}

export const DEFAULT_CHAT_ID = 'interview-1'

export function initialState(chatId = DEFAULT_CHAT_ID): ScratchpadState {
  return {
    chat_id: chatId,
    pending_request_id: 0,
    question: '',
    status: 'listening',
    short_answer: '',
    formula_or_structure: '',
    say_bullets: [],
    caveat: '',
    confidence: 0,
    version: 0,
    citations: [],
    transcript_tail: [],
    last_event_type: 'boot',
    updated_at: new Date().toISOString(),
  }
}

export function clampScratchpadPatch(raw: any, current: ScratchpadState): ScratchpadState {
  const normalizedBullets = Array.isArray(raw.say_bullets)
    ? raw.say_bullets.map((item: unknown) => String(item).trim()).filter(Boolean).slice(0, 3)
    : current.say_bullets

  const normalizedCitations = Array.isArray(raw.citations)
    ? raw.citations.map((item: unknown) => String(item).trim()).filter(Boolean).slice(0, 6)
    : current.citations

  const nextVersion = Number.isFinite(Number(raw.version))
    ? Math.max(current.version + 1, Number(raw.version))
    : current.version + 1

  const status = ['listening', 'draft', 'refined', 'final', 'stale'].includes(raw.status)
    ? raw.status
    : current.status

  return {
    ...current,
    question: String(raw.question ?? current.question ?? '').trim().slice(0, 240),
    status,
    short_answer: String(raw.short_answer ?? current.short_answer ?? '').trim().slice(0, 400),
    formula_or_structure: String(raw.formula_or_structure ?? current.formula_or_structure ?? '').trim().slice(0, 500),
    say_bullets: normalizedBullets,
    caveat: String(raw.caveat ?? current.caveat ?? '').trim().slice(0, 180),
    confidence: Math.max(0, Math.min(1, Number(raw.confidence ?? current.confidence ?? 0))),
    version: nextVersion,
    citations: normalizedCitations,
    updated_at: new Date().toISOString(),
  }
}

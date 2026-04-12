export const replyToolSchema = {
  type: 'object',
  properties: {
    chat_id: { type: 'string', description: 'Conversation id taken from the <channel ... chat_id="..."> tag.' },
    request_id: { type: 'integer', description: 'Echo the Request ID from the latest channel message exactly.' },
    question: { type: 'string', description: 'One-line cleaned interview question.' },
    status: {
      type: 'string',
      enum: ['listening', 'draft', 'refined', 'final', 'stale'],
      description: 'Scratchpad state.'
    },
    short_answer: { type: 'string', description: 'A concise answer, ideally 1-2 lines.' },
    formula_or_structure: { type: 'string', description: 'Most important formula, SQL skeleton, or checklist.' },
    say_bullets: {
      type: 'array',
      items: { type: 'string' },
      maxItems: 3,
      description: 'Up to 3 short bullets the user could say aloud.'
    },
    caveat: { type: 'string', description: 'One short caveat or assumption.' },
    confidence: { type: 'number', minimum: 0, maximum: 1, description: '0 to 1 confidence.' },
    version: { type: 'integer', description: 'Monotonic scratchpad version.' },
    citations: {
      type: 'array',
      items: { type: 'string' },
      description: 'Short source identifiers, such as topic names or relative file paths.'
    }
  },
  required: ['chat_id', 'request_id', 'question', 'status', 'short_answer', 'formula_or_structure', 'say_bullets', 'caveat', 'confidence']
} as const

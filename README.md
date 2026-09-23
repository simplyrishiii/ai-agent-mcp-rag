# Atlas Agent Lab

**Recruiter-facing AI systems engineering demo** that makes the system around the model visible.

![Zero key](https://img.shields.io/badge/demo-zero--key-0b1220?style=flat-square)
![Vercel](https://img.shields.io/badge/deploy-Vercel-0b1220?style=flat-square)
![CI](https://img.shields.io/badge/CI-smoke%20test-0b1220?style=flat-square)

## What it demonstrates

Atlas turns a user request into an inspectable workflow:

- intent + risk classification
- RAG-style retrieval with ranked local evidence
- MCP-style typed tool contracts
- prompt-injection gating before tool execution
- grounded answering and abstention
- latency, confidence, retrieval and risk telemetry
- a six-case deterministic evaluation harness
- zero-key browser operation

The repository also contains an **optional server-side Gemini adapter** at \`api/ask.js\`. The browser experience does not depend on it.

## Why this is a portfolio project

A generic chatbot mostly demonstrates that someone can wire up an API.

Atlas is designed to demonstrate that the developer understands the harder engineering questions around AI products: **how context is selected, how tools are constrained, how failures are surfaced, how grounding is measured, and how behavior is evaluated.**

## Architecture

\`\`\`text
User request
     │
     ▼
┌─────────────────────┐
│ Intent + risk gate  │  ← block before tools
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Retrieval + ranking │  ← evidence
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Tool router         │  ← typed capability
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Context compiler    │  ← sources + policy
└──────────┬──────────┘
           ▼
┌─────────────────────┐
│ Generation + verify │  ← grounded answer
└──────────┬──────────┘
           ▼
     telemetry + UI
\`\`\`

## Run locally

No build step is required:

\`\`\`bash
python -m http.server 8080
\`\`\`

Open \`http://localhost:8080\`.

Run the dependency-free smoke test:

\`\`\`bash
node tests/smoke.mjs
\`\`\`

## Project structure

\`\`\`text
.
├── index.html
├── api/ask.js
├── tests/smoke.mjs
├── .github/workflows/smoke.yml
├── .env.example
├── vercel.json
└── README.md
\`\`\`

## Scope boundaries

The default retrieval engine is **lexical**, not embedding-based. The tool layer is **MCP-style**, not a claim of a remote MCP server. These choices are deliberate: they keep the demo portable, deterministic and inspectable.

Clear upgrade paths include embeddings + vector search, a real MCP server, persistent memory, a model gateway, and distributed tracing.

## Optional live model

Set \`GEMINI_API_KEY\` in Vercel to enable the server-side adapter. Never commit secrets.

## Recruiter talking points

**AI engineering:** retrieval, orchestration, guardrails, tool contracts, abstention, evaluation, observability.

**Product thinking:** the interface exposes pipeline state rather than hiding everything behind a chat box.

**Production mindset:** zero-secret default, explicit failure states, lightweight CI, security headers, and documented limitations.

## License

MIT

# RelayOps AI

**Realistic AI support-operations copilot** for ticket triage, incident correlation, grounded response drafting, tool governance and human approval workflows.

## What the demo simulates

This is intentionally closer to a real internal SaaS operations console than a chatbot.

- enterprise support inbox with P1/P2/P3 tickets
- customer/account context and SLA state
- incident correlation across multiple tickets
- observability signals from a payments service
- RAG-style retrieval from support policies and incident records
- AI-generated case summary and customer response
- tool/action policy with a human approval gate
- explicit audit trail and agent execution trace
- deterministic browser runtime with no API key required

## Why this is more realistic

The AI is not presented as an autonomous chatbot. It sits inside an operational workflow where the important question is:

> What should the system do next, and what must a human approve?

The demo separates **analysis from external side effects**. The copilot can recommend escalation, retrieve evidence and prepare a response, but sending an external message or changing ticket state requires approval.

## Architecture

```text
Support ticket
     │
     ▼
┌──────────────────────┐
│ Triage + priority    │
│ customer/SLA context │
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Incident correlation │ ← related tickets + telemetry
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ RAG / evidence       │ ← policies + incident records
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Copilot decision     │ ← escalation + next action
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Draft response       │ ← grounded customer message
└──────────┬───────────┘
           ▼
┌──────────────────────┐
│ Approval gate        │ ← human before side effect
└──────────┬───────────┘
           ▼
     Audit + telemetry
```

## Recruiter talking points

**AI engineering:** RAG, evidence grounding, incident correlation, policy-aware tool use, abstention/approval gates and observability.

**Product thinking:** AI is embedded in a real operational workflow instead of being a standalone chat interface.

**Production mindset:** external actions are gated, decisions are auditable, customer context is visible, and the demo has clear boundaries.

## Run locally

```bash
python -m http.server 8080
```

Open `http://localhost:8080`.

## Scope

The current UI is a realistic deterministic simulation. The next production layer would connect the same interfaces to a real ticketing system, incident platform, knowledge base, model gateway and persistent audit store.

## License

MIT

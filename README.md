# AI Agent · MCP · RAG Lab

An interactive portfolio project demonstrating an AI-agent workflow with Retrieval-Augmented Generation (RAG), MCP-style tool routing, source grounding, and an observable execution trace.

## 🚀 Live Preview

**[Open the live interactive demo](https://ai-agent-mcp-rag.vercel.app/)**

> If the Vercel project has not yet been claimed/configured, open the repository's Vercel deployment and use the generated deployment URL shown there.

## What the demo shows

- **Agent orchestration** — intent classification → retrieval → tool routing → context assembly → generation/verification.
- **RAG** — retrieves ranked context from a small knowledge corpus before generating the answer.
- **MCP-style routing** — demonstrates how an agent can select an external capability rather than blindly answering.
- **Observability** — exposes the intermediate trace, retrieved chunks, scores, latency, and grounding confidence.
- **Responsive UI** — designed as a recruiter-facing interactive portfolio demo.

## Run locally

This is a zero-dependency static demo. Open `index.html` directly in a browser or serve the repository with any static web server.

## Deployment

The project is designed for Vercel's static hosting and requires no environment variables for the interactive demo.

## Architecture

```text
User question
     ↓
Intent classification
     ↓
Context retrieval / ranking
     ↓
MCP-style tool routing
     ↓
Grounded prompt assembly
     ↓
Generation + verification
     ↓
Answer + sources + trace
```

## Repository

[GitHub — simplyrishiii/ai-agent-mcp-rag](https://github.com/simplyrishiii/ai-agent-mcp-rag)

Built as an AI engineering portfolio project focused on agent orchestration, retrieval, tool interfaces, and production-oriented observability.

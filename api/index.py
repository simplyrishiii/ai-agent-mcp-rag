from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Import AI modules
from agents.rag_agent import RAGAgent
from agents.mcp_agent import MCPAgent
from utils.vector_store import VectorStore

load_dotenv()

app = FastAPI(
    title="AI Agent with MCP & RAG",
    description="Advanced AI system with Model Context Protocol and Retrieval-Augmented Generation",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize agents
rag_agent = RAGAgent(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    pinecone_api_key=os.getenv("PINECONE_API_KEY"),
    pinecone_environment=os.getenv("PINECONE_ENVIRONMENT")
)

mcp_agent = MCPAgent(
    mcp_server_url=os.getenv("MCP_SERVER_URL")
)

class QueryRequest(BaseModel):
    query: str
    use_mcp: bool = False
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: list
    confidence: float

@app.get("/")
async def root():
    return {
        "message": "AI Agent with MCP & RAG API",
        "status": "healthy",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/query", response_model=QueryResponse)
async def query(request: QueryRequest):
    try:
        if request.use_mcp:
            result = await mcp_agent.query(request.query)
        else:
            result = await rag_agent.query(
                query=request.query,
                top_k=request.top_k
            )
        
        return QueryResponse(
            answer=result.get("answer", ""),
            sources=result.get("sources", []),
            confidence=result.get("confidence", 0.0)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/index-documents")
async def index_documents(documents: list[dict]):
    try:
        for doc in documents:
            await rag_agent.add_document(doc)
        return {"status": "success", "message": f"Indexed {len(documents)} documents"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats")
async def get_stats():
    return {
        "indexed_documents": await rag_agent.get_document_count(),
        "vector_store": "pinecone",
        "mcp_enabled": True
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
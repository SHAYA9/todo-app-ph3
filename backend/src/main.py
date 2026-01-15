from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from src.agents.todo_agent import run_todo_agent
from src.database.config import init_db

app = FastAPI(title="AI Todo Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    conversation_id: Optional[int] = None
    message: str


class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[dict]


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()


@app.get("/")
async def root():
    return {
        "message": "AI Todo Chatbot API (Phase III)",
        "status": "running",
        "architecture": "Stateless with Database Persistence",
        "endpoints": {
            "chat": "/api/{user_id}/chat (POST)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy", "database": "connected"}


@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint(user_id: str, request: ChatRequest):
    """
    Stateless chat endpoint with database persistence
    
    Args:
        user_id: User identifier
        request: Chat request with message and optional conversation_id
    
    Returns:
        Chat response with conversation_id, response text, and tool calls
    """
    try:
        conversation_id, response, tool_calls = await run_todo_agent(
            user_id=user_id,
            user_message=request.message,
            conversation_id=request.conversation_id
        )
        
        return ChatResponse(
            conversation_id=conversation_id,
            response=response,
            tool_calls=tool_calls
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
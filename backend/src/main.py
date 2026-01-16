from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from src.agents.todo_agent import run_todo_agent
from src.database.config import init_db
from src.auth.routes import router as auth_router
from src.auth.dependencies import get_current_user
from src.database.models import User

app = FastAPI(title="AI Todo Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
                "http://localhost:3000",
                "http://localhost:3001",
                "http://127.0.0.1:3000",
                "http://127.0.0.1:3001",
                "https://chat-todo.vercel.app"
            ],    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Include auth routes
app.include_router(auth_router)


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


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    current_user: User = Depends(get_current_user)
):
    """
    Stateless chat endpoint with database persistence (requires authentication)
    
    Args:
        request: Chat request with message and optional conversation_id
        current_user: Authenticated user from dependency
    
    Returns:
        Chat response with conversation_id, response text, and tool calls
    """
    try:
        # Use authenticated user's ID
        user_id = str(current_user.id)
        
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


# Legacy endpoint (backward compatible, but deprecated)
@app.post("/api/{user_id}/chat", response_model=ChatResponse)
async def chat_endpoint_legacy(user_id: str, request: ChatRequest):
    """
    Legacy chat endpoint (deprecated - use /api/chat with authentication)
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
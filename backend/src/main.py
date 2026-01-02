from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from agent.main import run_agent
from typing import List, Optional

app = FastAPI(title="AI Todo Chatbot API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    message: str
    conversation_history: Optional[List[dict]] = None


@app.get("/")
async def root():
    return {
        "message": "AI Todo Chatbot API", 
        "status": "running",
        "endpoints": {
            "chat": "/chat (POST)",
            "health": "/health (GET)"
        }
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/chat")
async def chat_with_agent(msg: Message):
    response, updated_history = run_agent(
        msg.message, 
        msg.conversation_history
    )
    return {
        "response": response,
        "conversation_history": updated_history
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=5000)
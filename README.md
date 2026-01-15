# Phase III: AI Todo Chatbot

An AI-powered chatbot that manages todos through natural language using **OpenAI Agents SDK** and **MCP (Model Context Protocol)** architecture.

## 🏗️ Architecture

This project implements a **stateless, database-backed** architecture following Phase III specifications:

- **Frontend**: React with OpenAI ChatKit
- **Backend**: Python FastAPI
- **AI Framework**: OpenAI Agents SDK
- **MCP Server**: Official MCP SDK
- **Database**: SQLModel + Neon PostgreSQL (or SQLite locally)
- **Authentication**: Better Auth (optional)

### Architecture Diagram

```
┌─────────────────┐     ┌──────────────────────────────────────────────┐     ┌─────────────────┐
│                 │     │              FastAPI Server                   │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│  ChatKit UI     │────▶│  │         Chat Endpoint                  │  │     │    Neon DB      │
│  (Frontend)     │     │  │  POST /api/{user_id}/chat              │  │     │  (PostgreSQL)   │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │  - tasks        │
│                 │     │                  ▼                           │     │  - conversations│
│                 │     │  ┌────────────────────────────────────────┐  │     │  - messages     │
│                 │◀────│  │      OpenAI Agents SDK                 │  │     │                 │
│                 │     │  │      (Agent + Runner)                  │  │     │                 │
│                 │     │  └───────────────┬────────────────────────┘  │     │                 │
│                 │     │                  │                           │     │                 │
│                 │     │                  ▼                           │     │                 │
│                 │     │  ┌────────────────────────────────────────┐  │     │                 │
│                 │     │  │         MCP Server                     │  │────▶│                 │
│                 │     │  │  (MCP Tools for Task Operations)       │  │◀────│                 │
│                 │     │  └────────────────────────────────────────┘  │     │                 │
└─────────────────┘     └──────────────────────────────────────────────┘     └─────────────────┘
```

## 📊 Database Models

### Task
- `id`: Primary key
- `user_id`: User identifier (indexed)
- `title`: Task title
- `description`: Optional description
- `completed`: Boolean status
- `created_at`, `updated_at`: Timestamps

### Conversation
- `id`: Primary key
- `user_id`: User identifier (indexed)
- `created_at`, `updated_at`: Timestamps

### Message
- `id`: Primary key
- `user_id`: User identifier (indexed)
- `conversation_id`: Foreign key to Conversation
- `role`: "user" | "assistant" | "system"
- `content`: Message text
- `created_at`: Timestamp

## 🔧 MCP Tools

The MCP server exposes 5 tools for task management:

1. **add_task** - Create new task
2. **list_tasks** - Retrieve tasks (all/pending/completed)
3. **complete_task** - Mark task as complete
4. **delete_task** - Remove task
5. **update_task** - Modify task title/description

## 🚀 Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 16+
- OpenAI API Key
- Neon PostgreSQL account (or use SQLite locally)

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add:
   - `OPENAI_API_KEY`: Your OpenAI API key
   - `DATABASE_URL`: Your Neon PostgreSQL URL (optional, uses SQLite if not set)

5. **Initialize database**
   ```bash
   python migrations/init_db.py
   ```

6. **Run backend server**
   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload
   ```

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment**
   ```bash
   cp .env.local.example .env.local
   ```
   
   Edit `.env.local`:
   - `REACT_APP_BACKEND_API_URL`: Backend URL (default: http://localhost:5000)
   - `REACT_APP_USER_ID`: User ID for testing (default: demo_user)

4. **Run frontend**
   ```bash
   npm start
   ```

## 📝 API Endpoints

### POST /api/{user_id}/chat

Send a message and get AI response.

**Request**
```json
{
  "conversation_id": 1,  // Optional, creates new if not provided
  "message": "Add buy groceries"
}
```

**Response**
```json
{
  "conversation_id": 1,
  "response": "I've added 'buy groceries' to your tasks!",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": "{\"user_id\": \"demo_user\", \"title\": \"buy groceries\"}"
    }
  ]
}
```

## 💬 Natural Language Commands

- **Add**: "Add buy groceries", "Remember to call mom"
- **List**: "Show my tasks", "What's pending?"
- **Complete**: "Mark task 1 as done", "Complete the groceries task"
- **Delete**: "Delete task 2", "Remove the meeting"
- **Update**: "Change task 1 to buy milk", "Update groceries task"

## 🎯 Key Features

✅ **Stateless Architecture** - No server-side session storage  
✅ **Database Persistence** - All state in PostgreSQL/SQLite  
✅ **MCP Tools** - Standardized AI-to-app communication  
✅ **Conversation History** - Maintains context across sessions  
✅ **Multi-user Support** - User ID-based isolation  
✅ **Scalable** - Horizontal scaling ready  

## 🧪 Testing

Run backend tests:
```bash
cd backend
pytest tests/
```

## 📦 Deployment

### Backend (Vercel/Railway/Render)
1. Set environment variables (OPENAI_API_KEY, DATABASE_URL)
2. Deploy FastAPI app
3. Run database migrations

### Frontend (Vercel/Netlify)
1. Set REACT_APP_BACKEND_API_URL
2. For OpenAI ChatKit: Configure domain allowlist at https://platform.openai.com/settings/organization/security/domain-allowlist
3. Deploy React app

## 🔐 Environment Variables

### Backend (.env)
```env
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
```

### Frontend (.env.local)
```env
REACT_APP_BACKEND_API_URL=http://localhost:5000
REACT_APP_USER_ID=demo_user
REACT_APP_OPENAI_DOMAIN_KEY=...  # For production ChatKit
```

## 📚 Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | React + OpenAI ChatKit |
| Backend | Python FastAPI |
| AI Framework | OpenAI Agents SDK |
| MCP Server | Official MCP SDK |
| ORM | SQLModel |
| Database | Neon PostgreSQL / SQLite |
| Authentication | Better Auth (optional) |

## 🎓 Development Approach

Built using **Agentic Dev Stack workflow**:
1. ✅ Write spec
2. ✅ Generate plan
3. ✅ Break into tasks
4. ✅ Implement via Claude Code

## 📄 License

MIT

## 🤝 Contributing

Pull requests are welcome! Please follow the existing code structure and add tests for new features.
# AI Todo Chatbot

This project implements an AI-powered chatbot that allows users to manage their Todo list using natural language. It consists of a Python backend that hosts the AI agent and a React frontend for the chat interface.

## Features

- Add new tasks
- View all tasks (pending or completed)
- Mark tasks as complete or incomplete
- Delete tasks
- Update task descriptions

## Project Structure

- `backend/`: Python FastAPI application for the AI agent and integration with the MCP service.
- `frontend/`: React application for the user interface.
- `specs/`: Project specifications, plans, data models, contracts, and research documents.

## Setup Instructions

Follow these steps to set up and run the AI Todo Chatbot locally.

### Prerequisites

- Python 3.9+
- Node.js (LTS version) and npm
- An OpenAI API Key

### 1. Backend Setup

Navigate to the `backend/` directory and set up the Python environment.

```bash
cd backend
python -m venv venv
./venv/Scripts/activate # On Windows
# source venv/bin/activate # On macOS/Linux
pip install -r requirements.txt
```

#### Configuration

Create a `.env` file in the `backend/` directory based on `backend/.env.example`.

```ini
# backend/.env
OPENAI_API_KEY=your_openai_api_key_here
MCP_API_BASE_URL=http://localhost:8000 # Replace with your actual MCP API base URL if different
```

Replace `your_openai_api_key_here` with your actual OpenAI API key. Ensure `MCP_API_BASE_URL` points to your running FastAPI service (which is external to this project and assumed to be running).

#### Run Backend

Start the FastAPI application.

```bash
cd backend
./venv/Scripts/activate # On Windows
# source venv/bin/activate # On macOS/Linux
uvicorn src.main:app --host 0.0.0.0 --port 5000 --reload
```
The backend server will run on `http://localhost:5000`.

### 2. Frontend Setup

Navigate to the `frontend/` directory and install JavaScript dependencies.

```bash
cd frontend
npm install
```

#### Configuration

Create a `.env.local` file in the `frontend/` directory based on `frontend/.env.local.example`.

```ini
# frontend/.env.local
REACT_APP_BACKEND_API_URL=http://localhost:5000 # This should match your backend server address
```

#### Run Frontend

Start the React development server.

```bash
cd frontend
npm start
```
The frontend application will open in your browser, typically at `http://localhost:3000`.

## Usage

Once both the backend and frontend servers are running, open your web browser to `http://localhost:3000`.
You can interact with the AI Todo Chatbot using natural language in the chat interface.

**Example Commands:**

-   "Add a task to buy groceries"
-   "Show me my tasks"
-   "Show me my pending tasks"
-   "Mark task 1 as completed"
-   "Delete task 2"
-   "Update task 3 to review code"

Remember that for destructive actions like "delete task", the chatbot will ask for confirmation before proceeding.

## Running Tests

To run backend integration tests:

```bash
cd backend
./venv/Scripts/activate # On Windows
# source venv/bin/activate # On macOS/Linux
pytest tests/integration
```

## Linting and Formatting

### Backend (Python)

```bash
# Linting
cd backend
./venv/Scripts/activate # On Windows
# source venv/bin/activate # On macOS/Linux
flake8 src/

# Formatting (check only)
black --check src/
# Formatting (apply changes)
black src/
```

### Frontend (JavaScript/React)

ESLint is configured via `react-scripts`. Prettier is used for formatting.

```bash
# Formatting (check only)
cd frontend
npx prettier --check src/
# Formatting (apply changes)
npx prettier --write src/
```

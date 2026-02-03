# API Contracts: Todo Chatbot

## Backend API Endpoints

### Todos Management
- **GET** `/api/v1/todos` - Retrieve all todos
  - Response: `200 OK` with array of todo objects
  - Query Parameters: `page`, `limit`, `status`

- **POST** `/api/v1/todos` - Create a new todo
  - Request Body: `{ "title": "string", "description": "string", "status": "pending|completed" }`
  - Response: `201 Created` with created todo object

- **GET** `/api/v1/todos/{id}` - Retrieve specific todo
  - Response: `200 OK` with todo object or `404 Not Found`

- **PUT** `/api/v1/todos/{id}` - Update specific todo
  - Request Body: `{ "title": "string", "description": "string", "status": "pending|completed" }`
  - Response: `200 OK` with updated todo object

- **DELETE** `/api/v1/todos/{id}` - Delete specific todo
  - Response: `204 No Content` or `404 Not Found`

### Chatbot Endpoint
- **POST** `/api/v1/chatbot` - Process natural language request
  - Request Body: `{ "message": "string", "user_id": "string" }`
  - Response: `200 OK` with response object containing actions to perform

### Health Check
- **GET** `/health` - Check backend service health
  - Response: `200 OK` with health status

## Frontend API Consumption

### Environment Configuration
- `BACKEND_API_URL`: Base URL for backend API calls
- Used by frontend to make all API requests to backend

### Service Communication Pattern
- Frontend makes HTTP requests to backend via configured API URL
- Backend responds with JSON data
- Frontend updates UI based on API responses
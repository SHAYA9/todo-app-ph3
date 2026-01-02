# Data Model: AI Todo Chatbot

This document defines the data entities relevant to the AI Todo Chatbot feature, as understood from the perspective of the chatbot agent. The source of truth for this data is the external FastAPI service.

## Entity: Todo Task

Represents a single actionable item managed by the user.

### Attributes

| Attribute | Type | Description | Constraints |
|---|---|---|---|
| `id` | string | A unique identifier for the task. | Provided by the backend. |
| `description` | string | The text describing what needs to be done. | Required, max 1000 characters. |
| `status` | string | The current state of the task. | Must be one of: "pending", "completed". |

### State Transitions

- A task is created with a `status` of "pending".
- A "pending" task can transition to "completed".
- A "completed" task can transition back to "pending".
- A task can be deleted from any state.

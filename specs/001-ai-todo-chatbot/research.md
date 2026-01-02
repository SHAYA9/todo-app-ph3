# Research: AI Todo Chatbot

This document records the key architectural decisions for the AI Todo Chatbot feature.

## Decision: Agent-based vs. Rules-based Intent Parsing

-   **Decision**: Use an agent-based approach for intent parsing, specifically the OpenAI Agents SDK.
-   **Rationale**: The feature requires understanding natural language. An agent-based approach is more flexible and scalable than a rigid rules-based engine (e.g., regex, keyword matching). It can better handle variations in user phrasing and can be extended with new capabilities more easily. A rules-based system would be brittle and difficult to maintain as the number of intents grows.
-   **Alternatives considered**: A custom rules-based engine. This was rejected due to the high maintenance overhead and limited flexibility in understanding natural language nuances.

## Decision: Tool-based Execution vs. Direct API Calls

-   **Decision**: The agent will execute actions using a set of predefined tools, implemented with the MCP SDK. Each tool will correspond to an action a user can perform (e.g., `add_task`, `delete_task`).
-   **Rationale**: This decouples the agent's reasoning from the underlying API implementation. The agent's only job is to select the correct tool and extract the parameters. The tool handles the actual API call. This improves maintainability, as API changes only require updating the tool, not retraining or modifying the agent's core logic. It also enhances security and control by restricting the agent's actions to a well-defined set.
-   **Alternatives considered**: Allowing the agent to directly call the backend API. This was rejected as it gives the agent too much power and makes the system harder to debug and secure. Direct calls would require the agent to know about API endpoints, HTTP methods, and request/response formats, complicating its logic.

## Decision: Stateless Design

-   **Decision**: The chatbot will be stateless, holding no memory of the conversation or task list between sessions. All state will be fetched from the backend API on demand.
-   **Rationale**: A stateless design simplifies the architecture significantly. It eliminates the need for a session management layer and a database on the chatbot's side. This aligns with the constitution's principles of API-only integration and makes the application easier to scale and maintain.
-   **Alternatives considered**: A stateful design where the chatbot maintains conversation history or caches the task list. This was rejected due to the added complexity and the violation of the project's constitutional principle to rely solely on the backend for state.

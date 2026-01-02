<!--
Sync Impact Report:
- Version change: none -> 1.0.0
- List of modified principles: Initial creation
- Added sections: Core Principles, Technical Constraints, Development Workflow, Governance
- Removed sections: none
- Templates requiring updates:
  - ✅ .specify/templates/plan-template.md
  - ✅ .specify/templates/spec-template.md
  - ✅ .specify/templates/tasks-template.md
- Follow-up TODOs: none
-->
# Phase III Todo AI Chatbot Constitution

## Core Principles

### I. Spec-Driven Development (NON-NEGOTIABLE)
All behavior must be defined in specs before implementation.
No manual code edits are allowed.
Claude Code is the only implementation source.

### II. API-Only Integration
The AI chatbot must interact with the Todo system only via existing FastAPI APIs.
No database or model access is allowed.

### III. Agent-Based Reasoning
Natural language understanding must be handled via OpenAI Agents SDK.
Agents must detect intent, extract parameters, and select tools.

### IV. MCP Tool Execution
All task actions must be executed using Official MCP SDK tools.
Each tool maps one-to-one with a backend API endpoint.

### V. Safety & Confirmation
The chatbot must confirm destructive actions.
Ambiguous commands must trigger clarification questions.
No hallucinated task states are allowed.

### VI. Stateless Operation
The chatbot holds no long-term memory.
All task state must be fetched from backend APIs.

## Technical Constraints
- UI: OpenAI ChatKit
- Reasoning: OpenAI Agents SDK
- Tools: Official MCP SDK
- Backend: Existing FastAPI Todo API
- No auth, no schedulers, no DB changes

## Development Workflow
Specs -> Plan -> Tasks -> Implement
Iteration happens by refining specs only.

## Governance
This constitution overrides all other instructions.
Violations require spec correction, not code edits.

**Version**: 1.0.0
**Ratified**: 2025-12-30
**Last Amended**: 2026-01-02
---
id: 001
title: Establish Project Constitution v1.0.0
stage: constitution
date: 2026-01-02
surface: agent
model: gemini
feature: none
branch: master
user: USER_PLACEHOLDER
command: /sp.constitution
labels: [constitution,setup]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
 - .specify/templates/plan-template.md
 - .specify/templates/tasks-template.md
tests:
 - none
---

## Prompt

/sp.constitution # Phase III Todo AI Chatbot Constitution

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
**Last Amended**: 2025-12-30

## Response snapshot

Constitution v1.0.0 has been established and saved to `.specify/memory/constitution.md`. Dependent templates for planning and tasking have been updated to align with the new principles.

- **Version**: 1.0.0
- **Change**: Initial creation of the project constitution.
- **Impact**: Aligned project templates with core principles like API-only integration and agent-based reasoning.

## Outcome

- ✅ Impact: High. Established foundational principles for the project.
- 🧪 Tests: n/a
- 📁 Files: 3 files modified.
- 🔁 Next prompts: /sp.specify
- 🧠 Reflection: The provided constitution was detailed, allowing for precise updates to dependent templates. The changes ensure future planning and task generation will adhere to the new architectural constraints.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): null
- Next experiment (smallest change to try): n/a

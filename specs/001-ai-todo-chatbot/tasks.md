# Tasks: AI Todo Chatbot

**Input**: Design documents from `/specs/001-ai-todo-chatbot/`
**Prerequisites**: plan.md, spec.md, data-model.md, contracts/, research.md

**Tests**: The tasks below include integration tests to validate the end-to-end flow for each user story.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create backend/frontend project structure based on `plan.md`.
- [X] T002 [P] Initialize Python backend project with OpenAI Agents SDK and MCP SDK dependencies.
- [X] T003 [P] Initialize Javascript frontend project with OpenAI ChatKit dependency.
- [X] T004 [P] Configure linting and formatting tools for both backend and frontend projects.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 [Backend] Implement the MCP SDK client in `backend/src/services/mcp_client.py` to connect to the existing FastAPI service.
- [X] T006 [Backend] Set up the basic agent orchestrator in `backend/src/agent/main.py` using the OpenAI Agents SDK.
- [X] T007 [Backend] Implement a generic tool-calling and dispatch mechanism in the agent.
- [X] T008 [Frontend] Create the main chat UI component in `frontend/src/components/Chat.js`.
- [X] T009 [Frontend] Set up the main page at `frontend/src/pages/Index.js` to host the chat component.
- [X] T010 [Frontend] Implement API service to connect the frontend UI to the backend agent endpoint.

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel.

---

## Phase 3: User Story 1 - Add a new task (Priority: P1) 🎯 MVP

**Goal**: Allows a user to add a new task to their list via chat.

**Independent Test**: A user can type "add a task to buy milk" and see a confirmation. The new task should appear when viewing the list.

### Implementation for User Story 1

- [X] T011 [Backend] [US1] Implement the `add_task` tool in `backend/src/agent/tools/add_task.py`, which uses the `mcp_client` to call the backend.
- [X] T012 [Backend] [US1] Register and integrate the `add_task` tool with the agent orchestrator in `backend/src/agent/main.py`.
- [X] T013 [Test] [US1] Write an integration test to verify the add task flow from chat input to backend confirmation.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently.

---

## Phase 4: User Story 2 - View tasks (Priority: P1)

**Goal**: Allows a user to see all their tasks in the chat window.

**Independent Test**: A user with existing tasks can type "show my tasks" and the tasks are displayed.

### Implementation for User Story 2

- [X] T014 [Backend] [US2] Implement the `view_tasks` tool in `backend/src/agent/tools/view_tasks.py`.
- [X] T015 [Backend] [US2] Integrate the `view_tasks` tool with the agent.
- [X] T016 [Frontend] [US2] Implement UI logic in `frontend/src/components/Chat.js` to render the list of tasks returned by the agent.
- [X] T017 [Test] [US2] Write an integration test for the "view tasks" flow.

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently.

---

## Phase 5: User Story 3 - Mark task status (Priority: P2)

**Goal**: Allows a user to mark a task as complete or incomplete.

**Independent Test**: A user can say "I finished the milk task" and the task's status will be updated.

### Implementation for User Story 3

- [X] T018 [Backend] [US3] Implement the `mark_task_status` tool in `backend/src/agent/tools/mark_task_status.py`.
- [X] T019 [Backend] [US3] Integrate the `mark_task_status` tool with the agent.
- [X] T020 [Test] [US3] Write an integration test for the "mark task status" flow.

---

## Phase 6: User Story 4 - Delete a task (Priority: P3)

**Goal**: Allows a user to delete a task.

**Independent Test**: A user can say "delete the milk task", confirm, and the task is removed.

### Implementation for User Story 4

- [X] T021 [Backend] [US4] Implement the `delete_task` tool in `backend/src/agent/tools/delete_task.py`.
- [X] T022 [Backend] [US4] Implement the confirmation logic within the agent for destructive actions as specified in the spec.
- [X] T023 [Test] [US4] Write an integration test for the "delete task" flow, including the confirmation step.

---

## Phase 7: User Story 5 - Update a task (Priority: P3)

**Goal**: Allows a user to update the description of a task.

**Independent Test**: A user can say "change milk task to buy almond milk" and the description is updated.

### Implementation for User Story 5

- [X] T024 [Backend] [US5] Implement the `update_task` tool in `backend/src/agent/tools/update_task.py`.
- [X] T025 [Backend] [US5] Integrate the `update_task` tool with the agent.
- [X] T026 [Test] [US5] Write an integration test for the "update task" flow.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T027 [P] Documentation: Update `README.md` with final setup and usage instructions.
- [X] T028 Code cleanup and final review across all new files.
- [X] T029 Validate all steps in `quickstart.md` are accurate.

---

## Dependencies & Execution Order

- **Phase 1 (Setup)** must complete before all other phases.
- **Phase 2 (Foundational)** depends on Phase 1 and blocks all user story phases.
- **User Stories (Phases 3-7)** can be implemented in parallel after Phase 2 is complete.
- **Phase 8 (Polish)** depends on all user stories being complete.

---

## Implementation Strategy

### MVP First (User Story 1 & 2)

1.  Complete Phase 1: Setup
2.  Complete Phase 2: Foundational
3.  Complete Phase 3: User Story 1 (Add Task)
4.  Complete Phase 4: User Story 2 (View Tasks)
5.  **STOP and VALIDATE**: Test adding and viewing tasks independently. This forms the core MVP.

### Incremental Delivery

1.  Deliver MVP (US1 & US2).
2.  Add User Story 3 (Mark Status) → Test independently → Deploy/Demo.
3.  Add User Story 4 & 5 (Delete/Update) → Test independently → Deploy/Demo.

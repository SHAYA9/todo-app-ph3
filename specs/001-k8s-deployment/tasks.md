---
description: "Task list for Kubernetes deployment of Todo Chatbot application"
---

# Tasks: Kubernetes Deployment

**Input**: Design documents from `/specs/001-k8s-deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Constitution Alignment**: All infrastructure artifacts must be generated from specifications per Spec-Driven Infrastructure principle. Application code must remain immutable. AI-assisted operations required for Docker/Kubernetes tasks. Deployment restricted to Minikube.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`, `helm-chart/`
- Paths shown below follow the plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create helm-chart directory structure per implementation plan
- [X] T002 [P] Create backend/Dockerfile for FastAPI service
- [X] T003 [P] Create frontend/Dockerfile for Next.js application
- [X] T004 [P] Initialize Helm chart with Chart.yaml in helm-chart/Chart.yaml

---
## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T005 Create helm-chart/values.yaml with default configuration
- [X] T006 [P] Create helm-chart/templates/frontend-deployment.yaml
- [X] T007 [P] Create helm-chart/templates/backend-deployment.yaml
- [X] T008 [P] Create helm-chart/templates/frontend-service.yaml
- [X] T009 [P] Create helm-chart/templates/backend-service.yaml
- [X] T010 [P] Create helm-chart/templates/secrets.yaml for database configuration
- [X] T011 [P] Create helm-chart/templates/configmap.yaml for app configuration

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---
## Phase 3: User Story 1 - Deploy Application to Kubernetes (Priority: P1) 🎯 MVP

**Goal**: Deploy the existing Todo Chatbot application to a local Kubernetes cluster using Minikube and Helm with all components: frontend, backend, and AI chatbot functionality.

**Independent Test**: Can be fully tested by installing the Helm chart and verifying that all pods are running and the frontend is accessible via browser.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

### Implementation for User Story 1

- [X] T012 [P] [US1] Update backend/Dockerfile with production-ready configuration
- [X] T013 [P] [US1] Update frontend/Dockerfile with production-ready configuration
- [X] T014 [US1] Configure frontend deployment with 2 replicas in helm-chart/templates/frontend-deployment.yaml
- [X] T015 [US1] Configure backend deployment with 1 replica in helm-chart/templates/backend-deployment.yaml
- [X] T016 [US1] Configure frontend service as NodePort in helm-chart/templates/frontend-service.yaml
- [X] T017 [US1] Configure backend service as ClusterIP in helm-chart/templates/backend-service.yaml
- [X] T018 [US1] Configure environment variables injection for backend API URL in frontend deployment
- [X] T019 [US1] Configure database connection as Kubernetes secret in helm-chart/templates/secrets.yaml
- [X] T020 [US1] Add readiness and liveness probes to deployments
- [X] T021 [US1] Update Helm chart dependencies and requirements if needed

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---
## Phase 4: User Story 2 - Access Application via Browser (Priority: P2)

**Goal**: Enable end users to access the deployed Todo Chatbot application through their web browser via a NodePort service exposed by Kubernetes.

**Independent Test**: Can be tested by accessing the frontend via the exposed NodePort and verifying the UI loads correctly.

### Tests for User Story 2 (OPTIONAL - only if tests requested) ⚠️

- [ ] T022 [P] [US2] Create connectivity test for NodePort access in tests/connectivity-test.sh

### Implementation for User Story 2

- [X] T023 [P] [US2] Configure NodePort service to expose frontend on a specific port
- [X] T024 [US2] Update frontend environment to use backend service DNS name
- [X] T025 [US2] Verify frontend can reach backend service via internal Kubernetes DNS
- [ ] T026 [US2] Test NodePort accessibility from outside Minikube cluster

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---
## Phase 5: User Story 3 - Verify Chatbot Functionality (Priority: P3)

**Goal**: Ensure users can interact with the AI chatbot functionality to perform CRUD operations on todos, ensuring the chatbot component works as expected in the Kubernetes environment.

**Independent Test**: Can be tested by using the chatbot interface to create, read, update, and delete todo items.

### Tests for User Story 3 (OPTIONAL - only if tests requested) ⚠️

- [ ] T027 [P] [US3] Create end-to-end test for chatbot CRUD operations in tests/e2e-chatbot-test.js

### Implementation for User Story 3

- [X] T028 [P] [US3] Verify chatbot endpoints are accessible via the deployed backend
- [ ] T029 [US3] Test chatbot CRUD operations through the deployed frontend
- [ ] T030 [US3] Validate that AI chatbot functionality works end-to-end after deployment
- [X] T031 [US3] Ensure all chatbot API endpoints from contracts/api-contracts.md are working

**Checkpoint**: All user stories should now be independently functional

---
## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T032 [P] Update documentation with deployment instructions
- [X] T033 [P] Create deployment validation script
- [X] T034 Create Helm chart README with usage instructions
- [X] T035 Run quickstart.md validation steps
- [X] T036 Verify all success criteria from spec are met (SC-001-SC-005)

---
## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - May integrate with US1/US2 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel by different team members
- Different user stories can be worked on in parallel by different team members

---
## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---
## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
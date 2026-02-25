# Sprint Review Summary

This document summarizes the outcomes, validation results and feedback collected at the end of each sprint.

---

# Sprint 1 Review

### Sprint Goal
Establish the core architecture and implement functional task management functionality.

### Delivered Increment
At the end of Sprint 1, the system:

- Allowed task creation
- Allowed task editing
- Allowed basic task status updates
- Persisted data using SQLite
- Implemented a layered architecture (Controller, Service, Repository, Domain)

### Validation

- All selected user stories were completed
- Functional manual testing was performed 
- Core CRUD operations work correctly
- No critical defects were identified

### Feedback & Observations

- The system worked functionally but lacked strict business rule enforcement
- Status transistions were not yet controlled
- No automated testing was implemented
- Architecture was solid but required validation improvements

### Adaptation for Next Sprint

Sprint 2 will focus on:
- Enforcing controlled workflow transitions
- Implementing delete functionality 
- Introducing automated unit testing
- Strengtheing business logic validation

---

# Sprint 2 Review

### Sprint Goal
Implement task lifecycle management with controlled transitions and automated testing.

### Delivered Increment

At the end of Sprint 2, the system:

- Support task deletion
- Enforces controlled status transitions (todo -> doing -> done)
- Rejects invalid transistions
- Includes automated unit tests using pytest
- Uses an isolated in-memory database for testing
- Maintains clean layered architecture

### Validation

- All selected user stories were completed
- All unit tests pass successfully
- Manual testing confirmed workflow correctness
- No regression issues from Sprint 1 features

### Feedback & Observation

- Business logic is now properly enforced
- System reliability significantly improved
- Architecture proved scalable and maintainable
- Application is ready for UI/UX improvements

### Adaptation for Next Sprint

Sprint 3 will focus on:
- Implementing Kanban board visualization
- Improving user experience
- Enchacing UI interaction
- Refining status change visual feedback

---

# Sprint 3 Review

### Sprint Goal
Improve Kanban board visualization and user interaction without modifying business logic.

### Delivered Increment

At the end of Sprint 3, the system:

- Displays tasks in a professional Kanban board layout
- Groups tasks dynamically by status
- Shows task counters per column
- Restricts delete option to DONE tasks only
- Includes confirmation before deletion
- Uses Bootstrap 5 for enchanced UI layout
- Maintains controlled workflow validation

### Validation

- Manual testing performed for:
    - Task creation
    - Status transitions
    - Reopen flow
    - Delete with confirmation
- All previous automated tests still pass
- No regression detected from Sprint 2

### Feedback & Observations

- System now provides clear visual workflow tracking
- UI significantly improves user experience
- Architecture separation proved scalable
- Application now resembles real-world Kanban tools

### Adaptation for Next Sprint

Potential improvements:
- Drag and drop transitions
- Flash messages for invalid transitions
- Task priority indicators
- User authentication layer
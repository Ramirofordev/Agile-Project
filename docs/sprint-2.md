# Sprint 2

---

## Duration
1 week

---

## Sprint Goal
Implement task lifecycle management with controlled state transitions and automated testing to ensure business logic reliability.

---

## Select User Stories
- US-03 - Delete a Task
- US-04 - Controlled status transitions (Jira-style workflow)

---

## Functional Scope

### Delete a task
- Allow users to delete an existing task
- Ensure task is permanently removed from the database  
- Validate that the task exists before deletion
- Update the board automatically after deletion

### Controlled Status Transitions
Implement a Jira-style workflow with controlled transitions

#### Defined states
- todo
- doing
- done

#### Allowed transitions
- todo -> doing
- doing -> done
- done -> doing

#### Restricted transitions
- todo -> done
- done -> todo

All transitions rules are enforced in the Service Layer

---

## Technical tasks
- Implement delete_task() in TaskRepository
- Fix and implement update_status() in TaskRepository
- Implement transition validation logic in TaskService
- Add Flask route to task deletion
- Add Flask route for status updates
- Implement allowed transition dictionary in Service Layer
- Configure application to support testing environment
- Create a unit tests using pytest
- Use in-memory SQLite database for isolated testing

---

## Testing Coverage
- Delete Task
- Valid status transition
- Invalid status transition

All tests:
- Run with pytest
- Use SQLite in-memory database
- Do not affect production database
- Pass successfully 

---

## Architecture
The application maintains a clean separation of concerns:
- Flask (Controller Layer) - Handles HTTP requests and responses
- TaskService (Business Logic Layer) - Enforces workflow rules and validations
- TaskRepository (Persistence Layer) - Handles database Operations
- TaskModel (Domain Layer) - Represents the task entity

Principles applied:
- Single Responsibility Principle
- Separation of Concerns
- Clean Architecture approach
- Controlled business rules enforcement

---

## Increment Delivered
At the end of Sprint 2, the application:
- Supports full task lifecycle management
- Implements a controlled Jira-syle workflow
- Is protected by automated unit tests
- Is architecture prepared for UI and UX improvements in Sprint 3
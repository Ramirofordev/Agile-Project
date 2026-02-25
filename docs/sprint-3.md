# Sprint 3

---

## Duration
1 Days

---

## Sprint Goal

Improve user experience by implementing a professional Kanban board visualization while maintining the controlled workflow and business rules implemented in Sprint 2.

This sprint focuses on presentation layer implementations without modifying the core business logic.

---

### Select User Stories
- US-05 - Kanban board visualization
- US-06 - Improve Visual Status Feedback
- US-07 - Improve UX for status Actions

---

## Functional Scope

#### Kanban Board Visualization
- Tasks are grouped by status:
    - todo
    - doing
    - done
- Each state is displayed in a separate column
- Column headers are visually highlighted and displayed in uppercase
- Task counters are shown per column
- Tasks automatically appear in the correct column

---

## UI improvements

- Bootstrap 5 integrated for professional styling
- Responsive grid layout
- Styled task cards with hover effect
- Conditional description rendering (only if present)
- Delete button only visible in DONE column
- Confirmation dialog before deletion

---

## Workflow Integrity

- UI only displays valid transitions
- Backend continues enforcing business rules
- No changes made to:
    - TaskService
    - TaskRepository
    - Database schema
    - Workflow logic

---

## Technical tasks

- Create board.html template
- Integrate Bootstrap CDN
- Refactor index route to render board.html
- Implement Jinja status grouping logic
- Add confirmation dialog for deletion
- Ensure route compatibility with existing service logic

--- 

## Architecture Impact

This sprint enchances the Presentation Layer only.

The layered architecture remains intact:

- Flask (Controller Layer)
- TaskService (Business Logic Layer)
- TaskRepository (Persistence Layer)
- TaskModel (Domain Layer)

---

## Increment Delivered
 
At the end of Sprint 3, the application:

- Displays a professional Kanban board
- Clearly separates tasks by state
- Provides improved user interaction
- Maintains strict workflow validation
- Is portofolio-ready with production-style UI
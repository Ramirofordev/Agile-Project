# Sprint 4

---

## Duration 
2 days

---

## Sprint Goal

Introduce a user authentication system and implement drag-and-drop functionality
to enhance security and modernize user interaction while preserving the controlled
workflow enforced in previous sprints.

This sprint focuses on expanding the system architecture to support multi-user
capabilities and improving task interaction without compromising business logic integrity.

---

## Select User Stories

- US-08 - User Authentication System
- US-09 - Drag and Drop Task Movement

---

## Funtional Scope

### User Authentication System

- User registration with:
    - username
    - email
    - password
- Secure password hashing
- Login and logout functionality
- Session-based authentication
- Restrict board access to authenticated users only
- Associate each task with a specific user
- Users can only see and manage their own tasks

---

### Drag and Drop Task Movement

- Task become draggable within the Kanban board
- Tasks can only be dropped into valid columns
- Status updates occur dynamically
- Page refresh is not required for visual movement
- Backend continues enforcing controlled transitions
- Invalid transitions remain blocked at Service Layer

---

## Architecture Impact

Sprint 4 expands the system architecture by introducing:

- Authentication management layer
- Multi-user data isolation
- Task ownership validation

Layered structure remains consistent:

- Flask (Controller Layer)
- AuthService & TaskService (Business Logic Layer)
- Repositories (Persistence Layer)
- Domain Models (Task + User)

No business logic is implemented in the UI.

All workflow validations remain protected in the Service Layer.

---

## Security Considerations

- Passwords are securely hashed before storage
- Authentication required for board access
- Task ownership verified before modification
- Defensive programming applied at Service Layer
- No direct database access from routes

---

## Testing Strategy

- Unit tests for authentication flows
- Validation tests for task ownership
- Regressing testing for workflow transitions
- Ensure previous tests from Sprint 2 continue passing

--- 

## Increment Delivered

At the end of Sprint 4, the application:

- Supports secure multi-user authentication
- Restricts data visibility per user
- Maintains strict workflow validation
- Allows intuitive drag-and-drop task transitions
- Preserves clean layered architecture
- Moves closer to production-ready application standards
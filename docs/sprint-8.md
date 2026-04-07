# Sprint 8

## Duration 
2 Days

---

## Sprint Goal

Introduce structured task organization through Projects and Contexts, and improve overall usability by implementing responsive design.

The system evolves from a task-based board into a scalable productivity system.

---

## Sprint Objective

- Implement Project-based task organization
- Introduce Context classification for tasks
- Enable task filtering (Project + Context)
- Add Project progress tracking 
- Create Project detail view with scoped Kanban board
- Improve UI responsiveness across devices

---

## Selected User Stories

- US-17 - Project Management System
- US-18 - Task Context Classification
- US-19 - Project Progress Tracking
- US-20 - Project Detail View (Kanban scoped)
- Internal Improvement - Responsive Design

---

## Functional Scope

### Project Management

- Users can create projects with name and description
- Tasks can be assigned to a project 
- Projects are displayed in a dedicated view 
- Each project shows:
    - Total tasks
    - Completed tasks
    - Progress percentage

---

### Context Classification

- Tasks can include a context (e.g., home, work, computer)
- Context is user-specific
- Tasks can be filtered by context
- Contexts can be created dynamically

---

### Task Filtering System

- Dashboard supports filtering by:
    - Project
    - Context
- Filters can be combined
- Active filters are visually displayed
- Users can clear filters easily

---

### Project Detail View

- Each project has its own dedicated page
- Displays project progress
- Includes a scope Kanban board
- Only tasks belonging to the project are shown

---

### Responsive Design 

- Application adapts to mobile and tablet devices
- Navbar collapses correctly 
- Kanban board adjusts to:
    - 3 columns (desktop)
    - 2 columns (tablet)
    - 1 columns (mobile)
- Forms and controls reorganize vertically on small screens

---

## Technical Tasks

### Backend

- Create Project entity and relationship with Task
- Extend Task model with:
    - project_id
    - context_id
- Implement endpoints:
    - POST /projects
    - GET /projects
    - GEt /projects{id}
- Implement porject progress calculation
- Add filtering logic in service layer

---

### Frontend

- Project listing view
- Project creation modal
- Project detail view with Kanban integration
- Context selector in task form
- Filter system (Project + Context)
- Responsive layout improvements

---

## Architecture Impact

Sprint 8 extends the existing architecture without breaking separation of concerns.

- Service handle:
    - Project logic
    - Filtering logic
    - Progress calculation
- Repositories manage persistance
- UI remains free of business logic

The system scales while maintaining clean architecture principles.

---

## Delivered Increment

At the end of sprint 8, the application:

- Supports project-based task organization
- Allows context classification of tasks
- Provides advanced filtering capabilities
- Displays project-level progress
- Includes dedicated project views with Kanban boards
- Is fully usable on mobile devices
- Maintains consistency with existing gamification system

---

## Definition of Done (DoD)

- Features are implemented and manually tested
- No regression in previous functionality
- Code follows architectural principles
- Documentation is updated
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

---

# Sprint 4 Review

### Sprint Goal
Introduce secure user authentication and implement drag-and-drop task interaction while maintaining strict workflow validation and architectural integrity.

### Delivered Increment

At the end of Sprint 4, the system:

- Supports user registration and login
- Securely hashes user passwords
- Restricts board access to authenticated users
- Associates tasks with individual users
- Enforces task ownership validation
- Allows drag-and-drop task transitions
- Maintains controlled workflow rules in the Service Layer
- Preserves clean layered architecture

### Validation

- Authentication flows tested manually
- Task ownership verified across operations
- Drag-and-drop transitions validated against workflow rules
- Previous unit tests continue to pass
- No regression from previous sprints
- Additional tests added for authentication and ownership validation
- Invalid drag transitions handled without server crashes (400 controlled response)

### Feedback & Observations

- System security significantly improved
- Application now supports multi-user environments
- UX feels closer to real-world Kanban tools
- Architecture proved scalable for new layers
- Business logic remains protected and centralized  

### Adaptation for Next Sprint

Potential future improvements:

- Flash messaging for authentication feedback
- Password recovery funtionality
- Role-based access control (Admin/User)
- REST API endpoints for external integrations
- Deployment configuration (production-ready setup)

---

# Sprint 5 Review

### Sprint Goal

Implement gamification mechanics, hybrid priority logic and external API integration while preserving architectural and test reliability.

### Delivered Increment

At the end of Sprint 5, the system:

- Supports hybrid priority management (auto-escalation + manual override)
- Provides full REST API for taks management
- Assings Pokemon rewards upon task completion
- Integrates external Pokedex API
- Includes automated tests for API and reward logic
- Maintains clean layered architecture

### Validation

- 20 automated tests passing
- API endpoints validated
- Reward logic tested with mocked
- No regression from previous sprints
- Manual verification of gamification flow

### Feedback & Observations

- System evovled from simple CRUD app to gamified productivity tool
- Architecture proved scalable for new integrations
- Business logic remains centralized and protected
- Test coverage increased significantly

### Adaptation for Next Sprint

Potential improvements:

- Trainer level progression system
- Achievement system
- Production-ready deployment setup
- Timezone-aware datetime refactor
- Role-based access control
- Pomodoro implementation

---

# Sprint 6 Review

### Sprint Goal

Introduce productivity mechanics through a Pomodoro focus timer and expand the gamification system with
trainer progression and user statistics while maintaining architectural integrity and workflow validation.

### Delivered Increment

At the end of Sprint 6, the system:

- Implements a Pomodoro focus timer with selectable sessions durations
- Rewards XP upon completion of focus sessions
- Introduces a trainer level progression system
- Displays an XP progress bar indicating advancement to the next level
- Provides a trainer profile page showing productivity statistics
- Displays captured Pokemon in a personal collection view
- Integrates Pomodoro rewards with the existing gamification system
- Maintains strict workflow validation and layered architecture

### Validation

- Pomodoro timer behavior validated through manual testing
- XP reward endpoint verified after focus session completion
- Level progression confirmed after XP threshold is reached
- Trainer profile correctly displays user statistics
- Pokemon collection renders correctly in the trainer profile
- All previous automated tests continue to pass 
- No regression detected from Sprint 5 functionality

### Feedback & Observations

- Gamifiction mechanics significantly increased user engagement
- Trainer progression adds a long-term productivity incentive
- Architecture continues to scale without introducing coupling
- Service Layer successfully centralizes XP and reward logic
- UI improvements reinforce the productivity game theme

### Adaptation for Next Sprint

Potential improvements:

- Achievement / badge system
- Pokemon rarity and shiny mechanics
- Pokemon evolution system
- Improved test coverage for productivity mechanics
- Deployment configuration for production environment
- Performance optimization for API endpoints
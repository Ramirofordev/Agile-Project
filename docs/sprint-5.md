# Sprint 5

## Duration 
2 days

---

## Sprint Goal

Introduce gamification mechanics, implement a hybrid task priority system, and expose a REST API layer while maintining architecture integrity and strict business rule enforcement.

This sprint transforms the application into a gamified, test-driven productivity platform capable of interacting with external systems.

--- 

## Selected User Stories

- US-10 - Task Priority System
- US-11 - REST API for Tasks
- US-12 - Pokemon Reward System

---

## Functional Scope

### Hybrid Task Priority System

- Tasks support priority levels: low, medium, high
- Default priority is medium
- Automatic priority escalation based on task age
- Manual override prevents automatic changes
- Priority logic enforced in Service Layer
- Does not affect workflow transitions

---

### REST API Layer

Implemented full CRUD endpoints:

- GET /api/tasks
- GET /api/tasks/<id>
- POST /api/tasks
- PUT /api/tasks/<id>
- DELETE /api/tasks/<id>

All endpoints:
- Reuse Service Layer Logic
- Validate status transitions
- Return JSON responses
- Enforce authentication and ownership rules

---

### Pokemon Reward System

- Completing a task (doing -> done) triggers reward logic
- External Pokedex API integration
- Random Pokemon assigned to user
- Pokemon persisted in database
- Reward logic isolated in PokemonService
- External API calls mocked during testing

---

## Testing Strategy

- Unit tests for hybrid priority logic
- API endpoints tests (CRUD + validation)
- Reward system tests with mocking
- Owernship and authentication regression tests
- In-memory SQLite database for isolation

Total automated tests: 20+

All tests passing.

---

## Architecture Impact

Sprint 5 extends the system while preserving clean architecture:

- Flask (Controller Layer)
- TaskService & PokemonService (Business Logic Layer)
- Repositories (Persistence Layer) 
- Domain Models (Task, User, Pokemon)

No business logic implemented in UI.

All validations remain centralized in the Service Layer

---

## Incremented Delivered

At the end of sprint 5, the application:

- Implements a hybrid task priority system
- Exposes a fully functional REST API
- Integrates gamification via Pokemon rewards
- Maintains strict workflow validation
- Preserves multi-user data isolation
- Achieves full automated test coverage for core features
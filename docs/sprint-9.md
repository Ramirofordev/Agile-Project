# Sprint 9

## Duration
2 Days

---

## Sprint Goal

Prepare the application for a safe persistence migration from local SQLite to Supabase PostgreSQL while preserving the current Flask, SQLAlchemy, authentication, gamification and testing architecture.

The system evolves from a local-file persistence model into a production-ready database strategy suitable for Render deployments and future real-user usage.

---

## Sprint Objective

- Define the database migration strategy from SQLite to Supabase PostgreSQL
- Keep Flask and SQLAlchemy as the application backend foundation
- Avoid introducing Supabase Auth during the first migration phase
- Document required environment variables and deployment implications
- Identify risks related to avatars, local files, schema drift and tests
- Keep the current test strategy stable while production persistence changes

---

## Selected User Stories

- US-21 - Configure Supabase PostgreSQL Persistence
- US-22 - Replace Local Production SQLite with DATABASE_URL
- US-23 - Document Deployment Database Configuration
- US-24 - Evaluate Avatar Storage Migration

---

## Functional Scope

### Production Database Persistence

- The application should be able to use a managed PostgreSQL database in production.
- User accounts, tasks, projects, contexts, XP, Pokemon captures and profile preferences should survive Render restarts and redeployments.
- Local SQLite may remain available for development when no production database URL is configured.

---

### Deployment Configuration

- Render should provide the production database URL through an environment variable.
- The application should not depend on a local `kanban.db` file in production.
- Secrets and database credentials must remain outside the repository.

---

### Migration Safety

- The first phase should migrate only the database layer.
- Supabase Auth should not replace Flask-Login during this sprint.
- Supabase Storage should be evaluated separately for avatar persistence.
- Existing business rules must remain in the Service Layer.

---

### Testing Continuity

- Automated tests should continue using isolated in-memory SQLite unless PostgreSQL-specific behavior needs dedicated coverage.
- Existing tests must continue to validate services, ownership, CSRF, gamification and API behavior.
- External integrations should remain mocked where applicable.

---

## Technical Tasks

### Backend

- Introduce a production database configuration strategy based on `DATABASE_URL`.
- Preserve SQLite fallback for local development and test environments.
- Review current `ensure_schema()` behavior and document its limitations for PostgreSQL.
- Identify schema fields that must exist in Supabase before deployment.
- Keep Flask-Login as the authentication layer for the first migration phase.

---

### Database

- Create a Supabase PostgreSQL project for production persistence.
- Validate the equivalent schema for:
    - users
    - tasks
    - projects
    - contexts
    - pokemons
- Plan a transition from ad-hoc schema updates toward explicit migrations.
- Decide whether existing local data needs one-time migration or can start fresh.

---

### Deployment

- Configure Render with the Supabase `DATABASE_URL`.
- Confirm that local SQLite is no longer used by the production service.
- Document deployment rollback steps.
- Validate that no database credentials are committed.

---

### Documentation

- Create a Supabase migration plan.
- Update the product backlog with Sprint 9 migration stories.
- Update Definition of Done to include database change verification.

---

## Architecture Impact

Sprint 9 changes the production persistence strategy without changing the application architecture.

- Routes remain in `app.py`
- Business rules remain in `services/`
- SQLAlchemy models remain in `domain/`
- Repositories remain in `infraestructure/repositories/`
- Authentication remains based on Flask-Login
- Supabase is introduced as managed PostgreSQL, not as a full backend replacement

This keeps the migration incremental and reduces risk compared with rewriting the frontend, replacing authentication or splitting the app into separate frontend/backend deployments.

---

## Delivered Increment

At the end of Sprint 9, the application should have:

- A documented Supabase PostgreSQL migration plan
- A clear production database configuration strategy
- Updated backlog entries for migration work
- Database-related Definition of Done criteria
- A decision record that Supabase Auth and Storage are deferred to future phases

---

## Definition of Done (DoD)

- Migration scope is documented in English
- Production database configuration is clearly defined
- Risks and rollback strategy are documented
- Existing automated tests remain passing after implementation work
- No secrets or database credentials are committed
- Documentation is updated consistently with the existing project format

# Supabase Migration Plan

## Purpose

This document defines a safe, incremental plan to migrate the production database from local SQLite to Supabase PostgreSQL while keeping the current Flask and SQLAlchemy architecture.

The goal is not to rewrite the application. The goal is to make persistence reliable for deployment and real users.

---

## Current State

The application currently uses:

- Flask as the web framework
- Jinja templates for server-rendered pages
- SQLAlchemy models in `domain/`
- Repository classes in `infraestructure/repositories/`
- Business rules in `services/`
- Flask-Login for authentication
- SQLite as the default local database (`kanban.db`)
- In-memory SQLite for automated tests

The current production-style database file is created from the working directory:

```text
kanban.db
```

This is simple for local development, but it is risky for production deployments because Render filesystem persistence is not guaranteed unless a persistent disk is explicitly configured.

---

## Migration Goal

Use Supabase PostgreSQL as the production database while keeping:

- Flask
- SQLAlchemy
- Flask-Login
- Current service/repository/domain layering
- Existing tests using isolated SQLite where appropriate

Supabase should initially be treated as a managed PostgreSQL provider, not as a full application backend replacement.

---

## Non-Goals

The first migration phase does not include:

- Replacing Flask-Login with Supabase Auth
- Moving the frontend to Vercel
- Rewriting Jinja templates as React or Next.js
- Replacing the repository/service architecture
- Moving avatars to Supabase Storage immediately
- Implementing real-time features

These may be considered later, but they are intentionally outside the first migration scope.

---

## Why Supabase PostgreSQL

Supabase PostgreSQL is useful for this project because it provides:

- Managed PostgreSQL persistence
- Better reliability than local SQLite on Render
- A database dashboard for inspection and debugging
- A path toward future storage features for avatars
- Better production readiness for multiple users

---

## Recommended Architecture

```text
Browser
  |
  v
Render Flask App
  |
  v
SQLAlchemy
  |
  v
Supabase PostgreSQL
```

The frontend should remain server-rendered by Flask for now.

The recommended production setup is:

```text
Render + Flask + Supabase PostgreSQL
```

The following setup is not recommended yet:

```text
Vercel Frontend + Render Backend
```

That separation would require CORS, cookie/session changes, CSRF review and a larger frontend rewrite.

---

## Data That Must Persist

Supabase PostgreSQL should store:

- users
- tasks
- projects
- contexts
- Pokemon captures
- XP and level progress
- Pomodoro completion counters for authenticated users
- profile preferences:
    - display name
    - bio
    - focus goal
    - productivity resource label
    - productivity resource URL
    - avatar filename reference

Guest workspace data should remain local to the browser unless a future requirement says otherwise.

---

## Avatar Storage Note

Profile avatar files are currently stored in the application filesystem:

```text
static/uploads/avatars/
```

This is not ideal for Render production because uploaded files may be lost if the filesystem is recreated.

For Sprint 9, avatar storage should be documented as a risk. A future sprint can move avatar files to:

- Supabase Storage
- Cloudinary
- Another durable object storage provider

The database migration should not be blocked by avatar storage migration.

---

## Environment Variables

Production should use an environment variable similar to:

```text
DATABASE_URL=postgresql://...
```

The application normalizes PostgreSQL URLs to SQLAlchemy's `psycopg` driver format:

```text
postgresql+psycopg://...
```

This keeps Render/Supabase configuration simple while making the runtime driver explicit in the Flask application.

Render should provide this value securely.

The repository must not include:

- database passwords
- Supabase service keys
- connection strings
- `.env` files with real credentials

---

## Implementation Phases

### Phase 1 - Documentation and Planning

- Document the migration scope
- Update backlog items
- Identify database risks
- Confirm that Supabase is used only as PostgreSQL at first

### Phase 2 - Configuration Strategy

- App configuration prefers `DATABASE_URL` when present
- SQLite fallback remains available for local development
- In-memory SQLite remains available for tests
- PostgreSQL connection strings are normalized to the `psycopg` SQLAlchemy driver

### Phase 3 - Schema Preparation

- Create the equivalent PostgreSQL schema in Supabase
- Verify all SQLAlchemy models map correctly
- Review current `ensure_schema()` behavior
- Decide whether to introduce Alembic or Flask-Migrate for future schema changes

### Phase 4 - Deployment Validation

- Configure `DATABASE_URL` in Render
- Deploy to a test environment if available
- Register a user
- Create tasks, projects and contexts
- Complete task and Pomodoro flows
- Verify XP and Pokemon rewards persist after restart/redeploy

### Phase 5 - Data Migration, If Needed

- Decide whether local `kanban.db` data must be migrated
- If yes, export SQLite data and import into PostgreSQL carefully
- Validate user ownership and foreign keys
- Keep a backup of the original SQLite database

### Phase 6 - Future Storage Migration

- Evaluate moving avatars to Supabase Storage
- Update profile avatar upload logic
- Store durable public or signed URLs instead of local filenames

---

## Risks

### SQLite and PostgreSQL Differences

SQLite is permissive. PostgreSQL is stricter about types, constraints and SQL behavior.

Risk examples:

- Boolean defaults
- Date/time handling
- Foreign key constraints
- Auto-increment behavior
- Raw SQL in `ensure_schema()`

### Schema Drift

The application currently updates some schema fields through `ensure_schema()`.

This is acceptable for a small project, but production PostgreSQL should eventually use explicit migrations.

### Local Files

Avatar files stored in `static/uploads/avatars/` may not survive Render filesystem recreation.

### Secrets Management

Supabase credentials must stay in Render environment variables and never be committed.

---

## Rollback Strategy

If the Supabase migration causes production issues:

1. Keep the previous Render deployment available if possible.
2. Restore the previous `DATABASE_URL` or SQLite configuration.
3. Keep a backup of `kanban.db` before any data migration.
4. Avoid destructive schema operations until the new database is validated.
5. Roll back code and environment variables together.

---

## Validation Checklist

- [ ] Application boots with Supabase PostgreSQL
- [ ] User registration works
- [ ] Login/logout works
- [ ] Task CRUD works
- [ ] Project and context flows work
- [ ] Task status transitions still enforce business rules
- [ ] XP rewards persist
- [ ] Pokemon rewards persist
- [ ] Profile preferences persist
- [ ] Pomodoro completion rewards persist for authenticated users
- [ ] Guest workspace remains local-only
- [ ] Automated tests pass
- [ ] No credentials are committed

---

## Decision Summary

- Use Supabase PostgreSQL for production persistence.
- Keep Flask and SQLAlchemy.
- Keep Flask-Login for authentication.
- Keep Render as the single deployment target for the Flask app.
- Do not split frontend to Vercel yet.
- Defer Supabase Auth.
- Defer Supabase Storage for avatars to a later phase.

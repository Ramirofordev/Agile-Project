# Sprint 6 

## Duration 
2 Days

---

## Sprint Goal

Introduce a productivity support system through a Pomodoro focus timer and expand the gamification
mechanics with experience points, trainer progression and a personal trainer profile.

This sprint focuses on increasing user engagement while maintaining architectural consistency and protecting
the business rules implemented in previous sprints.

---

## Selected User Stories

- US-13 - Pomodoro Focus Timer
- US-14 - Pomodoro XP Reward
- US-15 - Trainer Level Progression
- US-16 - Trainer Profile page 

---

## Functional Scope

### Pomodoro Focus Timer

- Implement a focus timer based on the Pomodoro technique
- Users can start, pause and reset the timer
- Timer visually displays remaining time
- Multiple focus durations can be selected (25 / 30 / 45 minutes)
- Timer completion triggers XP rewards
- Pomodoro progress persists during the session

---

### Trainer XP and Level System

- Users gain XP when completing tasks
- Additional XP is granted when completing Pomodoro sessions
- Level progression follows a scaling formula
- Level increases automatically when XP threshold is reached
- XP bar visually represents progress toward the next level

--- 

### Trainer Profile Page

- Users can access a personal trainer profile page
- Display trainer statistics:
    - Level
    - Total XP
    - Tasks completed
    - Pomodoro sessions completed
- Shows all captured Pokemon in a grid-based collection view
- Newly captured Pokemon are visually highlighted

---

## Architecture Impact

Sprint 6 extends the system while preserving the existing layered architecture:

- Flask (Controller Layer)
- TaskService, UserProgressService & PokemonService (Business Logic Layer)
- Repositories (Persistance Layer)
- Domain Models (Task, User, Pokemon)

The Pomodoro timer logic remains client-side while XP rewards are validated through backend endpoints.

All productivity rewards and level calculations are centralized in the Service Layer.

--- 

## Gamification Impact

The application evolves into a productivity game system by introducing:

- Trainer progression
- XP reward mechanics
- Pomodoro productivity tracking
- Personal Pokemon collection

These features increase engagement without compromising system architecture.

---

## Testing Strategy

- Validation of Pomodoro completion endpoint
- XP reward verification for Pomodoro sessions
- Regression tests ensuring previous workflow rules remain intact
- Manual validation of timer behavior and UI integration
- Verification of XP bar updates after rewards

---

## Increment Delivered

At the end of Sprint 6, the application:

- Implements a functional Pomodoro productivity timer
- Rewards users with XP for focus sessions 
- Introduces a trainer level progression system
- Displays productivity statistics in a trainer profile page
- Show captured Pokemon in a personal collection view
- Maintains strict workflow validation and architectural integrity
- Preserves clean layered architecture while expanding gamification mechanics
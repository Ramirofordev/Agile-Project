# User Stories

---

## US-01 - Create a task

**As a** user
**I want** to create a new task
**So that** I can organize my activities

#### Acceptance Criteria:
- The task must include a title (required)
- The task must be stored in the database
- The task must appear in the task list

---

## US-02 - Edit a task

**As a** user
**I want** to edit an existing task
**So that** I can update incorrect or outdated information

#### Acceptance Criteria:
- The user must be able to modify the title and description
- Changes must be saved in the database
- The updated task must be reflected in the list

---

## US-03 - Delete a task

**As a** user
**I want** to delete an existing task
**So that** I can remove tasks that are no longer needed

#### Acceptance Criteria:
- The system must validate that the task exists
- The task must be permanently removed from the database
- The board must update automatically

---

## US-04 - Change task status

**As a** user
**I want** to change the status of a task following predefined rules
**So that** I can track progress consistently

#### Acceptance Criteria:
- Allowed states: todo, doing, done
- Only valid transitions permitted:
    - todo -> doing
    - doing -> done
    - done -> doing
- Invalid transitions must be rejected
- Transitions rules must be enforced in the Service Layer

---

## US-05 - Kanban Board Visualization

**As a** user 
**I want** to see my tasks organized in a Kanban-style board
**So that** I can visualize work progress clearly

#### Acceptance Criteria:
- Tasks must be grouped by state:
    - todo
    - doing 
    - done
- Each state must be displayed in a separate column 
- Tasks must appear automatically in the correct column 
- Status change must visually move the task between columns
- UI must not break existing lifecycle rules

---

## US-06 - Improve Visual Status Feedback

**As a** user
**I want** visual differentiation between tasks states
**So that** I can quickly understand progress

#### Acceptance Criteria:
- Each column must have clear visual labering
- Status buttons must be clearly displayed
- Status transitions must reflect immediately in UI
- Invalid transitions must show clear feedback messages

---

## US-07 - Improve UX for Status Actions

**As a** user
**I want** intuitive controls to move tasks
**So that** interaction feels similar to Jira

#### Acceptance Criteria:
- Buttons available only to move tasks
- UI must not show invalid transitions
- Backend still validates rules (defensive programming)
- Delete button only visible in DONE column
- Confirmation required before deletion

---

## US-08 - User Authentication System

**As a** user
**I want** to register and log into the system
**So that** I can securely manage my own tasks

#### Acceptance Criteria:
- Users must be able to register with:
    - username
    - email
    - password
- Passwords must be securely hashed
- Users must be able to log in
- Only authenticated can access the kanban board
- Users must only see their own tasks
- Users must be able to log out
- Authentication must not break existing task lifecycle logic

---

## US-09 - Drag and Drop Task Movement

**As a** user
**I want** to drag and drop tasks between Kanban columns
**So that** task movement feels intuitive and modern

#### Acceptance Criteria:
- Task must be draggable
- Tasks must only be dropped in valid columns
- Backend must validate transitions (defensive programming)
- Status must persist after page reload
- UI must update without breaking existing transitions rules

---

## US-10 - Task Priority System

**As a** user
**I want** to assign a priority level to my tasks
**So that** I can identify what is more important 

#### Acceptance Criteria:
- Task must support priority: low, medium, high
- Default priority: medium
- Priority must persist in DB
- Priority must auto-adjust based on task age (hybrid model)
- Manual override must prevent automatic escalation
- Priority must not break workflow transitions

---

## US-11 - REST API for Tasks

**As a** user
**I want** REST endpoints
**So that** external systems can interact with the application

#### Acceptance Criteria:
- GET /api/tasks
- GET /api/tasks/<id>
- POST /api/tasks
- PUT /api/tasks/<id>
- DELETE /api/tasks/<id>
- Must reuse Service Layer
- Must return JSON
- Must validate transitions

---

## US-12 - Pokemon Reward System

**As a** user
**I want** to receive a Pokemon when completing a Task
**So that** productivity feels rewarding

#### Acceptance Criteria:
- Completing task (doing -> done) triggers reward logic
- System consumes external Pokedex public API
- A random Pokemon is assigned to the user
- Pokemon is displayed in UI
- API failures handled gracefully
- Reward logic covered by automated tests (mocked integration)

---

## US-13 - Pomodoro Focus Timer

**As a** user
**I want** a focus timer
**So that** I can work in structured productivity sessions

#### Acceptance Criteria:

- The user must be able to start the timer
- The user must be able to pause the timer
- The user must be able to reset the timer
- The timer must display the remaining time visually
- The user must be able to select different focus duration (25 / 30 / 45 minutes)
- The timer must continue running until the sessions is completed or paused

---

## US-14 - Pomodoro XP Reward

**As a** user
**I want** to gain XP after completing a focus session
**So that** my productivity is rewarded

#### Acceptance Criteria:

- Completing a Pomodoro session must grant XP
- XP must be added to the user's total XP
- XP rewards must trigger level recalculation
- XP reward logic must be handled in the Service layer
- The XP bar must update after the reward is applied

---

## US-15 - Trainer Level Progression

**As a** user
**I want** to gain levels when earning XP
**So that** I can track my productivity progress

#### Acceptance Criteria:

- XP must accumulate across tasks and Pomodoro sessions 
- The system must calculate the XP required for the next level
- The user level must increase automatically when the threshold is reached
- The current level must be displayed in the UI
- The XP progress bar must reflect progress toward the next level

---

## US-16 - Trainer Profile Page

**As a** user
**I want** to access a personal trainer profile
**So that** I can see my productivity statistics and Pokemon collection

#### Acceptance Criteria:

- The user must be able to open the trainer profile page
- The profile must display:
    - Trainer level
    - Total XP
    - Tasks completed
    - Pomodoro sessions completed
- The profile must display all captured Pokemon
- Pokemon must appear in a grid-based layout
- Newly captured Pokemon must be visually highlighted

---

## US-17 - Project Management System

**As a** user
**I want** to create and manage projects
**So that** I can group related tasks and organize my work better

#### Acceptance Criteria:
- A project must have a name (required) and optional description
- The user must be able to create a project
- The user must be able to view a list of projects
- Tasks must be assignable to a project
- Only the owner can access their projects

---

## US-18 - Task Context Classification

**As a** user
**I want** to assign a context to tasks
**So that** I know where or how I can complete them

#### Acceptance Criteria:
- A task can have an optional context
- Contexts must belong to the user
- The user must be able to create contexts
- Tasks must display their context in the UI
- Tasks must be filterable by context

---

## US-19 - Project Progress Tracking

**As a** user
**I want** to see the progress of a project
**So that** I can track completion status


#### Acceptance Criteria:
- Progress must be calculated based on completed tasks
- Progress must be displayed as a percentage
- The UI must show:
    - Total tasks
    - Completed tasks
- Progress must update when task status changes

---

## US-20 - Project Detail View

**As a** user
**I want** to view a specific project
**So that** I can manage its tasks in isolation

#### Acceptance Criteria:
- The user must be able to open a project detail page
- The page must display:
    - Project name and description
    - Project progress
- The page must include a Kanban board
- Only tasks belonging to the project must be displayed

---
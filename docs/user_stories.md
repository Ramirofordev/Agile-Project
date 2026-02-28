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
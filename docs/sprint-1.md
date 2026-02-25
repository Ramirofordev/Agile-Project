# Sprint 1

## Duration
1 day

---

## Sprint Goal

Establish the core architecture and implement the foundational task management functionality, including task creation, editing and basic state handling

This sprint focuses on building a solid architectural base to support future lifecycle management and testing improvements.

---

# Selected User Stories
- US-01 - Create a Task
- US-02 - Edit a Task
- US-04 - Basic Task Status Update

---

## Functional Scope

#### Task Creation
- Allows users to create a new task
- Store the task in the database
- Display the task in the task list

#### Task Editing
- Allows users to modify task information
- Persist changes in the database
- Reflect updates in the UI

#### Basic Status Update
- Allows tasks to change status
- Store updated status in database

---

## Technical Tasks

- Create Task Model (Domain Layer)
- Implement TakeRepository (Persistance Layer)
- Implement TaskService (Business Logic Layer)
- Create Flask routes (Controller Layer)
- Create HTML templates
- Connect SQLite database

---

## Architecture Foundations

During this sprint, the application established a layered structure:

- Flask (Controller Layer)
- TaskService (Business Logic Layer)
- TaskRepository (Persistance Layer)
- TaskModel (Domain Layer)

This separation of concerns prepared the system for advanced lifecycle management and workflow validation implemented in Sprint 2.

---

## Incremented Delivered

At the end of Sprint 1, the application:

- Supported task creation and editing
- Persisted data in the database
- Displayed tasks in the UI
- Implemented a clean layered architecture
- Was prepared for controlled status transition and automated testing in sprint 2
# Sprint 8

## Duration


---

## Sprint Objective

Implement advance task organization features:
    * Create **projects containing tasks**
    * Add **context to tasks** (e.g., home, computer)

Secondary Improvements:
    * Responsive design
    * Website icon (favicon)

## Sprint Goal

Enable users to organize tasks within projects and classify them by context to improve productivity.

---

## User stories

🔴 **High Priority**

1. **Create projects with tasks**
**As a** user,
**I want** to create projects that contain multiple tasks,
**So I** can better organize my work.

Acceptance Criteria:
* A project can be created with name and description
* Tasks can be assigned to a project
* Tasks are viewable within a project 
* All projects can be listed


2. **Task Content**
**As a** user
**I want** to assign a context to each task (e.g., home, computer),
**So I** know where I can complete it.

Acceptance Criteria:
* A task has a *context* field
* Context can be selected or written
* Tasks can be filtered by context  

---

🟡 **Low Priority**

3. **Responsive design**
**As a user**,
**I want** to use the app on mobile devices,
**So I** can access it anywhere.

Acceptance Criteria: 
* Layout adapts to smaller screens
* Navigation is usable on mobile

4. **Website icon (favicon)**
**As a user**,
**I want** to see an icon in the browser tab, 
**So I** can easily identify the app.

Acceptance Criteria:
* Favicon is correctly displayed in the browser

---

## Technical Tasks

#### Backend
* Create *Project* entity
* Define relationship:
    * One project -> many tasks
* Update *Task* model:
    * Add *context* field
* Create endpoints: 
    * *POST /projects*
    * *GET /projects*
    * *GET /projects/{id}*
* Enable task association with projects 

#### Frontend 
* Views for:
    * Creating a project
    * Listing project 
    * Viewing tasks within a project 
* Add context input/selector for tasks
* Implement filtering by context

#### Definition of Done (DoD)
* Code follows SOLID principles 
* Features are manually tested 
* No existing functionality is broken
* Code is pushed to the repository 
* Documentation is updated 
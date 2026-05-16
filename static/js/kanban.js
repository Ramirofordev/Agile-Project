document.addEventListener("DOMContentLoaded", function () {

    const csrfToken = document.querySelector("meta[name='csrf-token']")?.content || "";
    const taskForm = document.getElementById("task-form");
    const isGuest = taskForm?.dataset.guest === "true";
    const guestStorageKey = "guestKanbanTasks";
    const csrfInput = csrfToken
        ? `<input type="hidden" name="csrf_token" value="${csrfToken}">`
        : "";

    const STATUS_BUTTONS = {
        todo: (id) => `
            <div class="d-grid mb-2">
                <button type="button" class="btn btn-outline-primary btn-sm task-edit-btn">
                    Edit
                </button>
            </div>

            <form action="/status/${id}/doing" method="post" class="d-grid">
                ${csrfInput}
                <button class="btn btn-warning btn-sm">Start</button>
            </form>
        `,

        doing: (id) => `
            <div class="d-grid mb-2">
                <button type="button" class="btn btn-outline-primary btn-sm task-edit-btn">
                    Edit
                </button>
            </div>

            <form action="/status/${id}/done" method="post" class="d-grid">
                ${csrfInput}
                <button class="btn btn-success btn-sm">Complete</button>
            </form>
        `,

        done: (id) => `
            <div class="d-grid mb-2">
                <button type="button" class="btn btn-outline-primary btn-sm task-edit-btn">
                    Edit
                </button>
            </div>

            <form action="/status/${id}/doing" method="post" class="mb-2 d-grid">
                ${csrfInput}
                <button class="btn btn-secondary btn-sm">Reopen</button>
            </form>

            <form action="/delete/${id}" method="post" class="d-grid">
                ${csrfInput}
                <button class="btn btn-danger btn-sm">Delete</button>
            </form>
        `
    };

    function priorityLabel(priority) {
        return priority === "high" ? "HIGH" : priority === "medium" ? "MEDIUM" : "LOW";
    }

    function getGuestTasks() {
        try {
            return JSON.parse(localStorage.getItem(guestStorageKey)) || [];
        } catch (error) {
            return [];
        }
    }

    function saveGuestTasks(tasks) {
        localStorage.setItem(guestStorageKey, JSON.stringify(tasks));
    }

    function updateEmptyMessage() {
        const emptyMessage = document.querySelector(".empty-board-message");
        if (!emptyMessage) return;

        const hasTasks = document.querySelectorAll(".task-card").length > 0;
        emptyMessage.classList.toggle("hidden", hasTasks);
    }

    function buildTaskCard(task) {
        const description = task.description
            ? `<p class="task-description"></p>`
            : "";

        const wrapper = document.createElement("div");
        wrapper.className = "card mb-3 task-card shadow-sm";
        wrapper.dataset.taskId = task.id;
        wrapper.dataset.priority = task.priority;
        wrapper.dataset.description = task.description || "";

        wrapper.innerHTML = `
            <div class="card-body">
                <h5></h5>
                <div class="task-priority priority-${task.priority}">${priorityLabel(task.priority)}</div>
                ${description}
                <div class="button-container">
                    ${STATUS_BUTTONS[task.status](task.id)}
                </div>
            </div>
        `;

        wrapper.querySelector("h5").textContent = task.title;

        const descriptionElement = wrapper.querySelector(".task-description");
        if (descriptionElement) {
            descriptionElement.textContent = task.description;
        }

        return wrapper;
    }

    function renderGuestTasks() {
        if (!isGuest) return;

        document.querySelectorAll(".task-list").forEach(list => {
            list.innerHTML = "";
        });

        getGuestTasks().forEach(task => {
            const targetList = document.querySelector(`.task-list[data-status="${task.status}"]`);
            if (targetList) {
                targetList.appendChild(buildTaskCard(task));
            }
        });

        updateCounters();
        updateEmptyMessage();
    }

    function updateGuestTask(taskId, updates) {
        const tasks = getGuestTasks().map(task => (
            task.id === taskId ? { ...task, ...updates } : task
        ));

        saveGuestTasks(tasks);
    }

    function deleteGuestTask(taskId) {
        saveGuestTasks(getGuestTasks().filter(task => task.id !== taskId));
    }

    function updateCounters() {

        document.querySelectorAll(".task-list").forEach(list => {

            const count = list.querySelectorAll(".task-card").length;

            const header =
                list.closest(".kanban-column")
                    .querySelector(".count");

            header.textContent = count;
        });

        updateEmptyMessage();
    }

    function moveTaskCard(taskElement, newStatus) {

        const targetList =
            document.querySelector(`.task-list[data-status="${newStatus}"]`);

        if (targetList) {
            targetList.appendChild(taskElement);
        }

        const id = taskElement.dataset.taskId;

        const container =
            taskElement.querySelector(".button-container");

        if (container && STATUS_BUTTONS[newStatus]) {
            container.innerHTML = STATUS_BUTTONS[newStatus](id);
        }

        if (isGuest) {
            updateGuestTask(id, { status: newStatus });
        }

        updateCounters();
    }

    function revertTaskCard(taskElement, previousList, previousIndex) {
        if (!previousList) return;

        const reference = previousList.children[previousIndex] || null;
        previousList.insertBefore(taskElement, reference);
        updateCounters();
    }

    async function handleTaskUpdate(taskId, newStatus, taskElement, previousList = null, previousIndex = null) {

        if (isGuest) {
            moveTaskCard(taskElement, newStatus);
            taskElement.classList.add("task-complete");
            setTimeout(() => {
                taskElement.classList.remove("task-complete");
            }, 600);
            return;
        }

        try {

            taskElement.classList.add("updating");

            const response = await fetch(`/status/${taskId}/${newStatus}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": csrfToken
                },
                body: JSON.stringify({
                    used_pomodoro: false
                })
            });

            if (!response.ok) {
                console.error("Task update failed");
                revertTaskCard(taskElement, previousList, previousIndex);
                taskElement.classList.remove("updating");
                return;
            }

            const data = await response.json();

            moveTaskCard(taskElement, newStatus);

            taskElement.classList.add("task-complete");
            setTimeout(() => {
                taskElement.classList.remove("task-complete");
            }, 600);

            if (data.total_xp !== undefined) {
                updateXPBar(data.total_xp, data.next_level_xp, data.level);
            }

            if (data.pokemon_name) {
                showCaptureAnimation(
                    data.pokemon_name,
                    data.pokemon_sprite,
                    data.pokemon_id,
                    data.is_shiny
                );
            }

        } catch (error) {

            console.error("Network error:", error);
            revertTaskCard(taskElement, previousList, previousIndex);

        } finally {

            taskElement.classList.remove("updating");

        }
    }

    document.querySelectorAll(".task-list").forEach(list => {

        new Sortable(list, {

            group: "kanban",

            animation: 150,

            onEnd: function (evt) {

                if (evt.from === evt.to) return;

                const taskId = evt.item.dataset.taskId;

                const newStatus = evt.to.dataset.status;

                handleTaskUpdate(
                    taskId,
                    newStatus,
                    evt.item,
                    evt.from,
                    evt.oldIndex
                );
            }
        });
    });

    taskForm?.addEventListener("submit", function (event) {
        if (!isGuest) return;

        event.preventDefault();

        const formData = new FormData(taskForm);
        const title = String(formData.get("title") || "").trim();

        if (!title) return;

        const task = {
            id: `guest-${Date.now()}`,
            title,
            description: String(formData.get("description") || "").trim(),
            priority: String(formData.get("priority") || "medium"),
            status: "todo"
        };

        const tasks = getGuestTasks();
        tasks.push(task);
        saveGuestTasks(tasks);

        const targetList = document.querySelector('.task-list[data-status="todo"]');
        if (targetList) {
            targetList.appendChild(buildTaskCard(task));
        }

        taskForm.reset();
        updateCounters();
    });

    document.addEventListener("submit", async function (e) {

        if (!e.target.matches("form[action^='/status/']")) return;

        e.preventDefault();

        const form = e.target;

        const action = form.getAttribute("action");

        const parts = action.split("/");

        const taskId = parts[2];

        const newStatus = parts[3];

        const taskElement =
            form.closest(".task-card");

        await handleTaskUpdate(
            taskId,
            newStatus,
            taskElement
        );
    });

    document.addEventListener("submit", async function (event) {
        if (!event.target.matches("form[action^='/delete/']")) return;

        event.preventDefault();

        const form = event.target;
        const taskElement = form.closest(".task-card");
        const taskId = taskElement?.dataset.taskId;

        if (!taskElement || !taskId) return;

        if (isGuest) {
            deleteGuestTask(taskId);
            taskElement.remove();
            updateCounters();
            return;
        }

        if (!confirm("Are you sure you want to delete this task?")) return;

        form.submit();
    });

    document.addEventListener("click", function (event) {
        const button = event.target.closest(".task-edit-btn");
        if (!button) return;

        const taskElement = button.closest(".task-card");
        if (!taskElement) return;

        document.getElementById("edit-task-id").value = taskElement.dataset.taskId;
        document.getElementById("edit-task-title").value = taskElement.querySelector("h5")?.textContent.trim() || "";
        document.getElementById("edit-task-description").value = taskElement.dataset.description || "";
        document.getElementById("edit-task-priority").value = taskElement.dataset.priority || "medium";

        bootstrap.Modal.getOrCreateInstance(document.getElementById("editTaskModal")).show();
    });

    document.getElementById("edit-task-form")?.addEventListener("submit", async function (event) {
        event.preventDefault();

        const taskId = document.getElementById("edit-task-id").value;
        const title = document.getElementById("edit-task-title").value.trim();
        const description = document.getElementById("edit-task-description").value.trim();
        const priority = document.getElementById("edit-task-priority").value;
        const taskElement = document.querySelector(`.task-card[data-task-id="${taskId}"]`);

        if (!title || !taskElement) return;

        if (!isGuest) {
            const response = await fetch(`/api/tasks/${taskId}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRF-Token": csrfToken
                },
                body: JSON.stringify({ title, description, priority })
            });

            if (!response.ok) return;
        } else {
            updateGuestTask(taskId, { title, description, priority });
        }

        taskElement.querySelector("h5").textContent = title;
        taskElement.dataset.description = description;
        taskElement.dataset.priority = priority;

        const oldDescription = taskElement.querySelector(".task-description");
        if (oldDescription) {
            oldDescription.remove();
        }

        if (description) {
            const descriptionElement = document.createElement("p");
            descriptionElement.className = "task-description";
            descriptionElement.textContent = description;
            taskElement.querySelector(".task-priority").after(descriptionElement);
        }

        const priorityElement = taskElement.querySelector(".task-priority");
        priorityElement.className = `task-priority priority-${priority}`;
        priorityElement.textContent = priorityLabel(priority);

        bootstrap.Modal.getInstance(document.getElementById("editTaskModal"))?.hide();
    });

    renderGuestTasks();

});

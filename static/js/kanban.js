document.addEventListener("DOMContentLoaded", function () {

    const STATUS_BUTTONS = {
        todo: (id) => `
            <div class="d-grid mb-2">
                <a href="/edit/${id}" class="btn btn-outline-primary btn-sm">
                    Edit
                </a>
            </div>

            <form action="/status/${id}/doing" method="post" class="d-grid">
                <button class="btn btn-warning btn-sm">Start</button>
            </form>
        `,

        doing: (id) => `
            <div class="d-grid mb-2">
                <a href="/edit/${id}" class="btn btn-outline-primary btn-sm">
                    Edit
                </a>
            </div>

            <form action="/status/${id}/done" method="post" class="d-grid">
                <button class="btn btn-success btn-sm">Complete</button>
            </form>
        `,

        done: (id) => `
            <div class="d-grid mb-2">
                <a href="/edit/${id}" class="btn btn-outline-primary btn-sm">
                    Edit
                </a>
            </div>

            <form action="/status/${id}/doing" method="post" class="mb-2 d-grid">
                <button class="btn btn-secondary btn-sm">Reopen</button>
            </form>

            <form action="/delete/${id}" method="post" class="d-grid">
                <button class="btn btn-danger btn-sm">Delete</button>
            </form>
        `
    };

    function updateCounters() {

        document.querySelectorAll(".task-list").forEach(list => {

            const count = list.querySelectorAll(".task-card").length;

            const header =
                list.closest(".kanban-column")
                    .querySelector(".count");

            header.textContent = count;
        });
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

        updateCounters();
    }

    async function handleTaskUpdate(taskId, newStatus, taskElement) {

        try {

            taskElement.classList.add("updating");

            const response = await fetch(`/status/${taskId}/${newStatus}`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    used_pomodoro: false
                })
            });

            if (!response.ok) {
                console.error("Task update failed");
                taskElement.classList.remove("updating");
                return;
            }

            const data = await response.json();

            moveTaskCard(taskElement, newStatus);

            taskElement.classList.add("task-complete");
            setTimeout(() => {
                taskElement.classList.remove("task-complete");
            }, 600);

            if (data.total_xp) {
                updateXPBar(data.total_xp, data.next_level_xp, data.level);
            }

            if (data.pokemon_name) {
                showCaptureAnimation(
                    data.pokemon_name,
                    data.pokemon_sprite,
                    data.pokemon_id
                );
            }

        } catch (error) {

            console.error("Network error:", error);

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
                    evt.item
                );
            }
        });
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

});
document.addEventListener("DOMContentLoaded", function () {

    const phases = [
        { type: "focus", duration: 25 },
        { type: "short_break", duration: 5 },
        { type: "focus", duration: 25 },
        { type: "short_break", duration: 5 },
        { type: "focus", duration: 25 },
        { type: "short_break", duration: 5 },
        { type: "focus", duration: 25 },
        { type: "long_break", duration: 15 }
    ];

    let currentPhaseIndex = 0;
    let remainingTime = phases[0].duration * 60;
    let interval = null;
    let cyclesCompleted = 0;

    const circle = document.querySelector(".progress-ring-circle");
    const timeDisplay = document.getElementById("pomodoro-time");
    const phaseDisplay = document.getElementById("pomodoro-phase");
    const cycleDisplay = document.getElementById("cycle-count");

    const focusSelect = document.getElementById("pomodoro-duration");

    const radius = 100;
    const circumference = 2 * Math.PI * radius;

    circle.style.strokeDasharray = circumference;
    circle.style.strokeDashoffset = 0;

    function setProgress(percent) {
        const offset = circumference - percent * circumference;
        circle.style.strokeDashoffset = offset;
    }

    function updateDisplay() {
        const minutes = Math.floor(remainingTime / 60);
        const seconds = remainingTime % 60;

        timeDisplay.textContent =
            `${String(minutes).padStart(2, "0")}:${String(seconds).padStart(2, "0")}`;
    }

    function applyPhaseStyle(type) {

        circle.classList.remove("focus-active", "break-active", "long-break-active");

        if (type === "focus") {
            circle.style.stroke = "#ef4444";
            circle.classList.add("focus-active");
            phaseDisplay.textContent = "Focus";
        }
        else if (type === "short_break") {
            circle.style.stroke = "#3b82f6";
            circle.classList.add("break-active");
            phaseDisplay.textContent = "Break";
        }
        else {
            circle.style.stroke = "#22c55e";
            circle.classList.add("long-break-active");
            phaseDisplay.textContent = "Long Break";
        }
    }

    async function completeFocusPhase() {

        const response = await fetch("/api/pomodoro/complete", {
            method: "POST"
        });

        const data = await response.json();

        if (data.total_xp !== undefined) {
            updateXPBar(data.total_xp, data.next_level_xp, data.level);
        }

        const sound = new Audio("/static/sounds/complete_cycle.mp3");
        sound.play().catch(()=>{});
    }

    function nextPhase() {

        if (phases[currentPhaseIndex].type === "focus") {
            completeFocusPhase();
        }

        currentPhaseIndex++;

        if (currentPhaseIndex >= phases.length) {
            currentPhaseIndex = 0;
            cyclesCompleted++;
            cycleDisplay.textContent = cyclesCompleted;
        }

        remainingTime = phases[currentPhaseIndex].duration * 60;

        applyPhaseStyle(phases[currentPhaseIndex].type);
        updateDisplay();
        setProgress(1);

        saveState();
    }

    function tick() {

        if (remainingTime > 0) {

            remainingTime--;

            const total = phases[currentPhaseIndex].duration * 60;
            setProgress(remainingTime / total);

            updateDisplay();
            saveState();
        }
        else {
            nextPhase();
        }
    }

    function start() {
        if (!interval) {
            interval = setInterval(tick, 1000);

            const sound = new Audio("/static/sounds/start_focus.mp3");
            sound.play().catch(()=>{});
        }
    }

    function pause() {
        clearInterval(interval);
        interval = null;
    }

    function reset() {

        pause();

        currentPhaseIndex = 0;
        remainingTime = phases[0].duration * 60;
        cyclesCompleted = 0;

        applyPhaseStyle("focus");
        updateDisplay();
        setProgress(1);

        cycleDisplay.textContent = 0;

        localStorage.removeItem("pomodoroState");
    }

    function saveState() {

        localStorage.setItem("pomodoroState", JSON.stringify({
            currentPhaseIndex,
            remainingTime,
            cyclesCompleted
        }));
    }

    function loadState() {

        const saved = localStorage.getItem("pomodoroState");
        if (!saved) return;

        const state = JSON.parse(saved);

        currentPhaseIndex = state.currentPhaseIndex;
        remainingTime = state.remainingTime;
        cyclesCompleted = state.cyclesCompleted;

        cycleDisplay.textContent = cyclesCompleted;

        applyPhaseStyle(phases[currentPhaseIndex].type);
        updateDisplay();

        const total = phases[currentPhaseIndex].duration * 60;
        setProgress(remainingTime / total);
    }

    document.getElementById("pomodoro-start").addEventListener("click", start);
    document.getElementById("pomodoro-pause").addEventListener("click", pause);
    document.getElementById("pomodoro-reset").addEventListener("click", reset);

    loadState();
    updateDisplay();
    applyPhaseStyle("focus");
    setProgress(1);

    focusSelect.addEventListener("change", function() {

        const minutes = parseInt(this.value);

        phases.forEach(p => {
            if (p.type === "focus") {
                p.duration = minutes;
            }
        });

        if (phases[currentPhaseIndex].type === "focus") {

            remainingTime = minutes * 60;

            updateDisplay();
            setProgress(1);

            saveState();
        }
    });

});
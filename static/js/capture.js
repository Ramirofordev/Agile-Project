function showCaptureAnimation(name, sprite, pokemonId, isShiny) {

    const overlay = document.getElementById("capture-overlay");
    const img = document.getElementById("capture-sprite");
    const pokeball = document.getElementById("pokeball-img");
    const nameText = document.getElementById("capture-name");
    const flash = document.getElementById("capture-flash");

    if (!overlay || !img || !pokeball || !nameText) return;

    // ===== PLAY SOUND SAFELY =====
    const sound = new Audio("/static/sounds/capture.mp3");
    sound.volume = 0.7;

    sound.play().catch(() => {
        document.addEventListener("click", () => {
            sound.play().catch(() => {});
        }, { once: true });
    });

    // ===== SHOW OVERLAY =====
    overlay.classList.remove("hidden");

    nameText.textContent = name.toUpperCase();

    // ===== POKEBALL SHAKE + FLASH =====
    setTimeout(() => {

        if (flash) {
            flash.classList.add("flash-active");

            // reset flash
            setTimeout(() => {
                flash.classList.remove("flash-active");
            }, 400);
        }

        setTimeout(() => {
            pokeball.style.display = "none";
            img.src = sprite;
            img.classList.remove("hidden");
        }, 150);

    }, 900);

    // ===== CLOSE OVERLAY =====

    if (pokemonId){
        localStorage.setItem("newPokemon", pokemonId);
    }

    setTimeout(() => {

        overlay.classList.add("hidden");

        pokeball.style.display = "block";
        img.classList.add("hidden");

        if (window.location.pathname === "/profile") {
            setTimeout(() => {
                location.reload();
            }, 200);
        }

        if (pokemonId) {
            const card = document.querySelector(
                `[data-pokemon-id="${pokemonId}"]`
            );

            if (card){
                card.classList.add("new-pokemon");
            }
        }

    }, 3000);
}
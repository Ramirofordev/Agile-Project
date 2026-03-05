document.addEventListener("DOMContentLoaded", () => {

    const bar = document.getElementById("xp-bar-fill");

    if(!bar) return;

    const xp = parseInt(bar.dataset.xp);
    const next = parseInt(bar.dataset.next);

    const percent = (xp / next) * 100;

    bar.style.width = percent + "%";

});

function updateXPBar(totalXP, nextLevelXP, level){

    const bar = document.querySelector(".xp-bar-fill");
    const text = document.querySelector(".xp-text");
    const levelText = document.getElementById("user-level");

    if(!bar) return;

    const percent = (totalXP / nextLevelXP) * 100;

    bar.style.width = percent + "%";

    setTimeout(() => {
        bar.classList.remove("xp-gain");
    }, 800);

    if(text){
        text.textContent = `${totalXP} / ${nextLevelXP} XP`;
    }

    if(levelText && level){
        levelText.textContent = level;
    }
}


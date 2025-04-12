const audio = document.getElementById("introAudio");

function playAudio() {
    if (audio) {
        audio.play().catch(err => {
            console.warn("Playback failed:", err);
        });
    }
}

function stopAudio() {
    if (audio) {
        audio.pause();
        audio.currentTime = 0;
    }
}

function closeIntro() {
    const modal = document.getElementById('introModal');
    modal.style.display = 'none';
    stopAudio();
}



/* home  */

document.addEventListener("DOMContentLoaded", () => {
    const tiles = document.querySelectorAll(".slide-tile");
    tiles.forEach((tile, index) => {
        tile.style.animationDelay = `${index * 0.2}s`;
    });
});


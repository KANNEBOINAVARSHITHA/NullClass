function enforceWatchLimit(limitInMinutes) {
    if (limitInMinutes === -1) return; // Unlimited
    setTimeout(() => {
        alert("Time's up! Upgrade your plan to continue watching.");
        // Optional: Pause video
        document.getElementById('videoPlayer').pause();
    }, limitInMinutes * 60 * 1000);
}

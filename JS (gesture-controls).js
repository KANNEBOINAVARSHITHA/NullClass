const video = document.getElementById("myVideo");
const container = document.getElementById("video-container");
const commentSection = document.getElementById("comment-section");

let lastTap = 0;
let tapCount = 0;
let tapTimeout;

container.addEventListener("click", (e) => {
  const now = new Date().getTime();
  const tapX = e.clientX;
  const tapRegion = getTapRegion(tapX);

  if (now - lastTap < 400) {
    tapCount += 1;
  } else {
    tapCount = 1;
  }
  lastTap = now;

  clearTimeout(tapTimeout);
  tapTimeout = setTimeout(() => {
    handleGesture(tapCount, tapRegion);
    tapCount = 0;
  }, 400);
});

function getTapRegion(x) {
  const width = window.innerWidth;
  if (x < width * 0.33) return 'left';
  if (x > width * 0.66) return 'right';
  return 'center';
}

function handleGesture(count, region) {
  if (count === 1 && region === 'center') {
    // Single tap center → Play/Pause
    if (video.paused) video.play();
    else video.pause();
  }
  else if (count === 2 && region === 'right') {
    // Double tap right → Forward 10s
    video.currentTime += 10;
  }
  else if (count === 2 && region === 'left') {
    // Double tap left → Backward 10s
    video.currentTime -= 10;
  }
  else if (count === 3 && region === 'center') {
    // Triple tap center → Next video
    alert("Next video triggered (replace with actual logic)");
    // Load next video here
  }
  else if (count === 3 && region === 'right') {
    // Triple tap right → Close site
    window.close();
  }
  else if (count === 3 && region === 'left') {
    // Triple tap left → Toggle comment section
    commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
  }
}

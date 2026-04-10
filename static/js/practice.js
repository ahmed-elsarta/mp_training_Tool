// ─── State ───────────────────────────────────────────────────────────────────

let duration = 0;
let timeLeft = 0;
let timerInterval = null;
let correctCount = 0;
let totalCount = 0;

let currentAudio = null;
let replayUsed = false;

let currentSide = null;
let answered = false;

// ─── Session Start ────────────────────────────────────────────────────────────

function startSession(seconds) {
  duration = seconds;
  timeLeft = seconds;

  document.getElementById("duration-screen").style.display = "none";
  document.getElementById("practice-screen").style.display = "block";

  updateTimerDisplay();
  timerInterval = setInterval(tick, 1000);
  nextQuestion();
}

// ─── Timer ────────────────────────────────────────────────────────────────────

function tick() {
  timeLeft--;
  updateTimerDisplay();
  if (timeLeft <= 0) endSession();
}

function updateTimerDisplay() {
  const minutes = Math.floor(timeLeft / 60)
    .toString()
    .padStart(2, "0");
  const seconds = (timeLeft % 60).toString().padStart(2, "0");
  document.getElementById("timer").textContent = `${minutes}:${seconds}`;
}

// ─── Question Builder ─────────────────────────────────────────────────────────

function pickRandom(arr) {
  return arr[Math.floor(Math.random() * arr.length)];
}

function nextQuestion() {
  answered = false;
  replayUsed = false;

  // Hide feedback, hide replay
  document.getElementById("feedback").style.display = "none";
  document.getElementById("replay-section").style.display = "none";
  document.getElementById("replay-btn").textContent = "🔁 Replay (1 left)";
  document.getElementById("replay-btn").disabled = false;

  // Reset button styles
  document.getElementById("btn-left").style.backgroundColor = "";
  document.getElementById("btn-right").style.backgroundColor = "";

  // Pick a random pair
  const pair = pickRandom(PAIRS);

  // Randomly decide which of the two to play
  const playWord = Math.random() < 0.5 ? pair.word : pair.partner;
  const distractorWord = playWord === pair.word ? pair.partner : pair.word;

  // Shuffle which side the correct answer appears on
  const correctOnLeft = Math.random() < 0.5;
  currentSide = correctOnLeft ? "left" : "right";

  if (correctOnLeft) {
    document.getElementById("label-left").textContent = playWord.text;
    document.getElementById("label-right").textContent = distractorWord.text;
  } else {
    document.getElementById("label-left").textContent = distractorWord.text;
    document.getElementById("label-right").textContent = playWord.text;
  }

  // Play audio
  const audioUrl = MEDIA_URL + "audio/" + playWord.audio_file.split("/").pop();
  // const audioUrl = playWord.audio_url;
  currentAudio = new Audio(audioUrl);
  currentAudio.play();

  // Show replay button after audio ends
  currentAudio.addEventListener("ended", () => {
    document.getElementById("replay-section").style.display = "block";
  });
}
// ─── Replay ───────────────────────────────────────────────────────────────────

function replayAudio() {
  if (replayUsed || !currentAudio) return;
  replayUsed = true;
  document.getElementById("replay-btn").textContent = "🔁 Replayed";
  document.getElementById("replay-btn").disabled = true;
  currentAudio.currentTime = 0;
  currentAudio.play();
}

// ─── Answer ───────────────────────────────────────────────────────────────────

function answer(side) {
  if (answered) return;
  answered = true;
  totalCount++;

  const isCorrect = side === currentSide;
  if (isCorrect) correctCount++;

  // Update score display
  document.getElementById("correct-count").textContent = correctCount;
  document.getElementById("total-count").textContent = totalCount;

  // Visual feedback on buttons
  const correctBtn =
    currentSide === "left"
      ? document.getElementById("btn-left")
      : document.getElementById("btn-right");
  const wrongBtn =
    currentSide === "left"
      ? document.getElementById("btn-right")
      : document.getElementById("btn-left");

  correctBtn.style.backgroundColor = "#4CAF50"; // green
  if (!isCorrect) wrongBtn.style.backgroundColor = "#f44336"; // red

  // Feedback text
  const feedbackEl = document.getElementById("feedback");
  document.getElementById("feedback-text").textContent = isCorrect
    ? "✓ Correct!"
    : "✗ Wrong!";
  feedbackEl.style.display = "block";

  // Next question after short delay
  setTimeout(() => {
    if (timeLeft > 0) nextQuestion();
  }, 1000);
}

// ─── Keyboard (F and J) ───────────────────────────────────────────────────────

document.addEventListener("keydown", (e) => {
  if (document.getElementById("practice-screen").style.display === "none")
    return;
  if (e.key === "f" || e.key === "F") answer("left");
  if (e.key === "j" || e.key === "J") answer("right");
});

// ─── End Session ──────────────────────────────────────────────────────────────

function endSession() {
  clearInterval(timerInterval);

  document.getElementById("practice-screen").style.display = "none";
  document.getElementById("done-screen").style.display = "block";

  // POST score to Django
  fetch("/practice/save-score/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": getCookie("csrftoken"),
    },
    body: JSON.stringify({
      minimal_pair_id: MINIMAL_PAIR_ID,
      correct: correctCount,
      total: totalCount,
      duration_chosen: duration,
    }),
  })
    .then((response) => response.json())
    .then((data) => {
      if (data.status === "ok") {
        window.location.href = `/practice/results/?correct=${correctCount}&total=${totalCount}&duration=${duration}`;
      }
    });
}

// ─── CSRF Helper ──────────────────────────────────────────────────────────────

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    document.cookie.split(";").forEach((cookie) => {
      const c = cookie.trim();
      if (c.startsWith(name + "=")) {
        cookieValue = decodeURIComponent(c.substring(name.length + 1));
      }
    });
  }
  return cookieValue;
}

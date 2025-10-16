let mediaRecorder;
let audioChunks = [];
let userName = "";
let userEmail = "";
let userActive = false;

// Ask name/email once when page loads
window.addEventListener("DOMContentLoaded", () => {
  const startBtn = document.getElementById("start-btn");

  startBtn.addEventListener("click", () => {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!name || !email) {
      alert("Please enter your name and email first.");
      return;
    }

    userName = name;
    userEmail = email;
    userActive = true;

    // Switch to chat section
    document.getElementById("user-info").classList.add("hidden");
    document.getElementById("chat-section").classList.remove("hidden");
    document.getElementById("status").innerText = `Hi ${name}! Tap the mic to ask your question.`;
  });
});

// Mic button — toggle recording
document.getElementById("mic-btn").addEventListener("click", async () => {
  if (!userActive) {
    alert("Please enter your name and email first.");
    return;
  }

  if (!mediaRecorder || mediaRecorder.state === "inactive") {
    startRecording();
  } else {
    stopRecording();
  }
});

async function startRecording() {
  const micBtn = document.getElementById("mic-btn");
  const status = document.getElementById("status");

  try {
    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
    mediaRecorder = new MediaRecorder(stream);
    audioChunks = [];

    mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);

    mediaRecorder.onstop = async () => {
      const audioBlob = new Blob(audioChunks, { type: "audio/webm" });
      await sendAudioToBackend(audioBlob);
    };

    mediaRecorder.start();
    micBtn.classList.add("recording");
    status.innerText = "Recording... tap again to stop.";
  } catch (err) {
    alert("Microphone access denied.");
    console.error(err);
  }
}

function stopRecording() {
  mediaRecorder.stop();
  document.getElementById("mic-btn").classList.remove("recording");
  document.getElementById("status").innerText = "Processing your question...";
}

async function sendAudioToBackend(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob);
  formData.append("name", userName);
  formData.append("email", userEmail);

  try {
    const response = await fetch("http://localhost:8000/api/query", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) throw new Error("Backend error");

    const blob = await response.blob();
    const audioUrl = URL.createObjectURL(blob);

    const audioElement = document.getElementById("response-audio");
    audioElement.src = audioUrl;
    audioElement.classList.remove("hidden");

    // Attempt playback after user interaction
    try {
      await audioElement.play();
      document.getElementById("status").innerText = "Response ready. Playing...";
    } catch (err) {
      console.warn("Autoplay blocked — showing play button instead.", err);
      document.getElementById("status").innerText = "Tap play to hear the response.";
    }

  } catch (error) {
    console.error(error);
    document.getElementById("status").innerText = "Error communicating with backend.";
  }
}

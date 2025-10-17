let mediaRecorder;
let audioChunks = [];
let userName = "";
let userEmail = "";
let userActive = false;
let chatHistory = []; // stores all queries

// Page load: ask name/email once
window.addEventListener("DOMContentLoaded", () => {
  document.getElementById("start-btn").addEventListener("click", () => {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();

    if (!name || !email) {
      alert("Please enter your name and email first.");
      return;
    }

    userName = name;
    userEmail = email;
    userActive = true;

    document.getElementById("user-info").classList.add("hidden");
    document.getElementById("chat-section").classList.remove("hidden");
    document.getElementById("status").innerText = `Hi ${name}! Tap the mic to ask your question.`;
  });
});

// 🎙 Mic button toggle
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
    status.innerText = "🎤 Recording... tap again to stop.";
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

    // Try autoplay
    try {
      await audioElement.play();
      document.getElementById("status").innerText = "✅ Response ready. Playing...";
    } catch (err) {
      document.getElementById("status").innerText = "▶️ Tap play to hear the response.";
    }

    // Store chat history (useful for summary)
    chatHistory.push({
      questionTime: new Date().toISOString(),
      user: userName,
      email: userEmail,
    });

  } catch (error) {
    console.error(error);
    document.getElementById("status").innerText = "⚠️ Error communicating with backend.";
  }
}

window.addEventListener("DOMContentLoaded", () => {
  const endChatBtn = document.getElementById("end-chat-btn");

  if (endChatBtn) {
    console.log("✅ End Chat button found, listener attached.");
    endChatBtn.addEventListener("click", async () => {
      console.log("🟡 End Chat clicked");

      if (!userName || !userEmail) {
        alert("Please enter your name and email first.");
        return;
      }

      const formData = new FormData();
      formData.append("name", userName);
      formData.append("email", userEmail);

      try {
        const response = await fetch("http://localhost:8000/api/end_chat", {
          method: "POST",
          body: formData,
        });

        const data = await response.json();
        if (data.status === "success") {
          alert("✅ Chat ended and summary email sent!");
          location.reload();
        } else {
          alert("⚠️ Chat ended but email failed to send.");
        }
      } catch (err) {
        console.error("❌ Error during end chat:", err);
        alert("Error ending chat. See console for details.");
      }
    });
  } else {
    console.error("❌ End Chat button not found in DOM!");
  }
});




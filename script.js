function addMessage(sender, text) {
  const chatbox = document.getElementById("chatbox");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message " + (sender === "You" ? "user" : "bot");

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;

  const timestamp = document.createElement("div");
  timestamp.className = "timestamp";
  const now = new Date();
  timestamp.textContent = now.toLocaleTimeString();

  messageDiv.appendChild(bubble);
  messageDiv.appendChild(timestamp);
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;
}
function getAnswerFromFAQ(question, faqData) {
  const lowerQuestion = question.toLowerCase();  // Convert user input to lowercase for case-insensitive matching

  // Iterate through the FAQ dataset
  for (const item of faqData) {
    // Create a regular expression from the FAQ question, making it case-insensitive
    // We escape special characters in the question to avoid regex syntax errors
    const regex = new RegExp(item.question.toLowerCase().replace(/[.*+?^=!:${}()|\[\]\/\\]/g, "\\$&"), 'i');
    
    // Test if the user's question matches the FAQ question using regex
    if (regex.test(lowerQuestion)) {
      return { text: item.answer, followUps: item.followUps || [] };
    }
  }

  // If no match is found, return a fallback answer
  return { text: "Sorry, I couldn't understand that. Can you rephrase?" };
}
function getAnswerFromChatGPT(question) {
  // This function is a placeholder for the actual ChatGPT API call
  // In a real implementation, you would replace this with an API request to OpenAI's ChatGPT
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({ text: "This is a response from ChatGPT.", followUps: [] });
    }, 1000);
  });
}

function typeBotResponse(fullText, followUps = []) {
  const chatbox = document.getElementById("chatbox");
  const messageDiv = document.createElement("div");
  messageDiv.className = "message bot";

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = "";

  messageDiv.appendChild(bubble);
  chatbox.appendChild(messageDiv);
  chatbox.scrollTop = chatbox.scrollHeight;

  let index = 0;

  function typeChar() {
    if (index < fullText.length) {
      const char = fullText.charAt(index);
      bubble.innerHTML += char === '\n' ? '<br>' : char;
      index++;
      chatbox.scrollTop = chatbox.scrollHeight;
      setTimeout(typeChar, 20); // Typing speed
    } else {
      const timestamp = document.createElement("div");
      timestamp.className = "timestamp";
      const now = new Date();
      timestamp.textContent = now.toLocaleTimeString();
      messageDiv.appendChild(timestamp);
      chatbox.scrollTop = chatbox.scrollHeight;

      if (followUps.length > 0) {
        addFollowUpButtons(followUps);
      }
    }
  }

  typeChar();
}

function addFollowUpButtons(questions) {
  const chatbox = document.getElementById("chatbox");
  const buttonContainer = document.createElement("div");
  buttonContainer.className = "follow-up-buttons";

  questions.forEach(q => {
    const btn = document.createElement("button");
    btn.className = "follow-up-btn";
    btn.textContent = q;
    btn.onclick = () => {
      document.getElementById("userInput").value = q;
      sendMessage();
    };
    buttonContainer.appendChild(btn);
  });

  chatbox.appendChild(buttonContainer);
  chatbox.scrollTop = chatbox.scrollHeight;
}

function sendMessage() {
  const input = document.getElementById("userInput");
  const message = input.value.trim();
  if (!message) return;

  addMessage("You", message);
  input.value = "";
  document.getElementById("thinking-indicator").style.display = "block";

  fetch("/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question: message })
  })
    .then(response => response.json())
    .then(data => {
      const delay = Math.random() * 2000;
      setTimeout(() => {
        document.getElementById("thinking-indicator").style.display = "none";
        typeBotResponse(data.answer, data.followUps || []);
      }, delay);
    })
    .catch(err => {
      console.error("Error:", err);
      document.getElementById("thinking-indicator").style.display = "none";
      addMessage("Bot", "Sorry, something went wrong!");
    });
}

// ✅ Send message on Enter key
document.addEventListener("DOMContentLoaded", function () {
  document.getElementById("userInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
      sendMessage();
    }
  });
});

document
  .getElementById("chat-form")
  .addEventListener("submit", async function (e) {
    e.preventDefault();
    const userInput = document.getElementById("user-input").value;

    addMessage("user-message", userInput);

    document.getElementById("user-input").value = "";

    try {
      const response = await fetch(
        "http://localhost:5005/webhooks/rest/webhook",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ sender: "user", message: userInput }),
        }
      );

      const messages = await response.json();

      messages.forEach((message) => {
        if (message.text) {
          addMessage("bot-message", message.text);
        }
      });
    } catch (error) {
      console.error("Mesaj gönderilirken bir hata oluştu:", error);
      addMessage("bot-message", "Bir hata oluştu, lütfen tekrar deneyin.");
    }
  });

function addMessage(type, text) {
  const chatBox = document.getElementById("chat-box");
  const messageDiv = document.createElement("div");

  messageDiv.classList.add("message", type);
  messageDiv.textContent = text;

  chatBox.appendChild(messageDiv);

  chatBox.scrollTop = chatBox.scrollHeight;
}

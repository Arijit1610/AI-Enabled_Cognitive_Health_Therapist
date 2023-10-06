document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const messageContainer = document.getElementById("message-container");

    sendButton.addEventListener("click", sendMessage);

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Clear the input field
        messageInput.value = "";

        // Create a new message element and display it
        displayMessage("You: " + message, "user");

        // Send the message to the Flask backend
        fetch("/send", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ message: message }),
        })
            .then(response => response.json())
            .then(data => {
                // Display the bot's response
                displayMessage("Bot: " + data.message, "bot");
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    function displayMessage(text, sender) {
        const messageElement = document.createElement("div");
        messageElement.textContent = text;
        messageElement.classList.add(sender);
        messageContainer.appendChild(messageElement);
    }
});

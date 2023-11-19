document.addEventListener("DOMContentLoaded", function () {
    const messageInput = document.getElementById("message-input");
    const sendButton = document.getElementById("send-button");
    const messageContainer = document.getElementById("message-container");

    // Function to send a greeting message automatically
    function sendGreeting() {
        const greetingMessage = "Hello, I'm your friendly chatbot. How can I assist you today?";
        displayMessage("Bot: " + greetingMessage, "bot");
    }

    // Call the sendGreeting function to send the initial greeting message
    sendGreeting();

    sendButton.addEventListener("click", sendMessage);

    function sendMessage() {
        const message = messageInput.value.trim();
        if (!message) return;

        // Clear the input field
        messageInput.value = "";

        // Create a new message element and display it
        displayMessage("You: " + message, "user"); // Note that the sender is "user" here

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
                displayMessage("Bot: " + data.message, "bot"); // The sender is "bot" for bot's messages
            })
            .catch(error => {
                console.error("Error:", error);
            });
    }

    function displayMessage(text, sender) {
        const messageElement = document.createElement("li");
        messageElement.textContent = text;
        messageElement.classList.add(sender); // Add the sender class
        messageContainer.appendChild(messageElement);
    }
});

//     function displayMessage(text, sender) {
//         const messageElement = document.createElement("li");
//         messageElement.className = sender; // Add 'user' or 'bot' class to the new element
//         messageElement.textContent = text;
//         messageContainer.appendChild(messageElement);
//     }
// });

const chatbot = document.getElementById('chatbot');

const msgbtn = () => {
    chatbot.style.display = "block";
}

const cbtn = () => {
    chatbot.style.display = "none";
}

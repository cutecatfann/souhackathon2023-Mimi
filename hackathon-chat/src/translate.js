// Get a reference to the "Shakespeareify" button
const shakespeareifyButton = document.getElementById("shakespeareify-button");

// Add an event listener to listen for clicks on the "Shakespeareify" button
shakespeareifyButton.addEventListener("click", () => {
  // Get the text from the input field
  const messageInput = document.getElementById("message");
  const text = messageInput.value;

  // Send the text to the Flask server to translate it to Shakespearean English
  fetch("/translate", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ text: text }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Display the translation in the chat area
      const message = data.message;
      addMessage(message);
    })
    .catch((error) => {
      console.error(error);
    });

  // Clear the input field
  messageInput.value = "";
});

// Function to add a message to the chat area
function addMessage(message) {
  // Get a reference to the chat area
  const messages = document.getElementById("messages");

  // Create a new message element
  const messageElement = document.createElement("li");
  messageElement.textContent = message;

  // Append the message element to the chat area
  messages.appendChild(messageElement);
}

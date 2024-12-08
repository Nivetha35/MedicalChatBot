const chatInput = document.querySelector(".chat-input textarea");
const sendChatBtn = document.querySelector(".chat-input span");
const chatbox = document.querySelector(".chatbox");
let userMessage;

const createChatLi = (message, className) => {
    const chatLi = document.createElement("li");
    chatLi.classList.add("chat", className);
    let chatContent = className === "outgoing" ? <p>${message}</p> : <span class="material-symbols-outlined">smart_toy</span><p>${message}</p>;
    chatLi.innerHTML = chatContent;
    return chatLi;
}

const handleChat = async () => {
    userMessage = chatInput.value.trim();
    if (!userMessage) return;
    chatbox.appendChild(createChatLi(userMessage, "outgoing"));
    chatInput.value = "";

    const response = await fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    const botMessage = data.response;

    chatbox.appendChild(createChatLi(botMessage, "incoming"));
}

sendChatBtn.addEventListener("click", handleChat);

chatInput.addEventListener("keypress", (event) => {
    if (event.key === "Enter") {
        handleChat();
    }
});
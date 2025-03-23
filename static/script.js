document.querySelector(".ipt").addEventListener("keydown", function (e) {
    if (e.key === "Enter") {
        e.preventDefault();
        sendMessage();
    }
});

document.addEventListener("DOMContentLoaded", function () {
    let chatDisplay = document.getElementById("chatDisplay");

    // 创建系统消息
    let welcomeMessage = document.createElement("div");
    welcomeMessage.classList.add("chat-message", "system");
    welcomeMessage.textContent = "🎧 欢迎使用智能耳机助手！";

    // 添加到聊天窗口
    chatDisplay.appendChild(welcomeMessage);
});

function sendMessage() {
    const inputField = document.querySelector(".ipt");
    const message = inputField.value.trim();
    if (!message) return;
    appendMessage("你", message, "user");
    inputField.value = "";

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message }),
    })
        .then((response) => response.json())
        .then((data) => {
            appendMessage("系统", data.reply, "system");
        })
        .catch((error) => {
            console.error("Error:", error);
            appendMessage("系统", "请求错误，请检查后端服务是否正常运行。", "system");
        });
}

function appendMessage(sender, text, type) {
    const chatDisplay = document.getElementById("chatDisplay");
    const messageDiv = document.createElement("div");
    messageDiv.className = "chat-message " + type;
    messageDiv.innerHTML = `<strong>${sender}:</strong> ${text.replace(
        /\n/g,
        "<br>"
    )}`;
    chatDisplay.appendChild(messageDiv);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

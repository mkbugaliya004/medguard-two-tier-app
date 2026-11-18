document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#ai-chat-form");
    const input = document.querySelector("#ai-chat-input");
    const messages = document.querySelector("#ai-chat-messages");
    const sendButton = document.querySelector("#ai-send-button");
    const includeAssessment = document.querySelector("#ai-include-assessment");

    if (!form || !input || !messages || !sendButton) return;

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        const message = input.value.trim();
        if (!message) return;

        addChatMessage("user", "You", message);
        input.value = "";
        sendButton.disabled = true;
        sendButton.textContent = "Thinking…";

        const assessment = includeAssessment?.checked
            ? (window.medguardLatestAssessment || null)
            : null;

        try {
            const result = await askMedGuardAI(message, assessment);
            addChatMessage("assistant", "MedGuard AI", result.answer || "No answer was returned.");
        } catch (error) {
            console.error("MedGuard AI error:", error);
            addChatMessage("assistant", "MedGuard AI", error.message || "Sorry, the AI request failed. Please try again.");
        } finally {
            sendButton.disabled = false;
            sendButton.textContent = "Send message →";
            input.focus();
        }
    });

    function addChatMessage(role, name, content) {
        const article = document.createElement("article");
        article.className = `ai-message ${role}`;

        const heading = document.createElement("strong");
        heading.textContent = name;

        const paragraph = document.createElement("p");
        paragraph.textContent = content;

        article.append(heading, paragraph);
        messages.appendChild(article);
        messages.scrollTop = messages.scrollHeight;
    }
});

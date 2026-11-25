document.addEventListener("DOMContentLoaded", async () => {
  try {
    const response = await fetch("/api/v1/auth/me", { credentials: "same-origin" });
    if (!response.ok) {
      window.location.replace("/login");
      return;
    }
    const user = await response.json();
    const avatar = document.querySelector(".profile-avatar");
    if (avatar) {
      avatar.textContent = (user.username || "admin").slice(0, 2).toUpperCase();
      avatar.title = user.username || "admin";
    }
    const topbar = document.querySelector(".topbar-right");
    if (topbar && !document.querySelector("#logout-button")) {
      const button = document.createElement("button");
      button.id = "logout-button";
      button.type = "button";
      button.className = "button button-secondary";
      button.textContent = "Logout";
      button.addEventListener("click", async () => {
        button.disabled = true;
        try {
          await fetch("/api/v1/auth/logout", { method: "POST", credentials: "same-origin" });
        } finally {
          window.location.replace("/login");
        }
      });
      topbar.appendChild(button);
    }
  } catch (error) {
    console.error("Session check failed:", error);
    window.location.replace("/login");
  }
});

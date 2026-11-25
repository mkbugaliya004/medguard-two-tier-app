document.addEventListener("DOMContentLoaded", async () => {
  const form = document.querySelector("#login-form");
  const error = document.querySelector("#login-error");
  const password = document.querySelector("#password");
  const toggle = document.querySelector("#toggle-password");

  toggle.addEventListener("click", () => {
    const reveal = password.type === "password";
    password.type = reveal ? "text" : "password";
    toggle.textContent = reveal ? "Hide" : "Show";
    toggle.setAttribute("aria-label", reveal ? "Hide password" : "Show password");
  });

  // Existing sessions should go straight to the dashboard.
  try {
    const session = await fetch("/api/v1/auth/me", { credentials: "same-origin" });
    if (session.ok) {
      window.location.replace("/");
      return;
    }
  } catch (e) {
    console.warn("Could not check existing MedGuard session.", e);
  }

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    error.textContent = "";
    const button = form.querySelector('button[type="submit"]');
    button.disabled = true;
    button.textContent = "Signing in…";

    try {
      const response = await fetch("/api/v1/auth/login", {
        method: "POST",
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          username: form.username.value.trim(),
          password: form.password.value
        })
      });
      const data = await response.json().catch(() => ({}));
      if (!response.ok) throw new Error(data.detail || "Unable to sign in.");
      window.location.replace("/");
    } catch (e) {
      error.textContent = e.message || "Login failed. Please try again.";
      button.disabled = false;
      button.innerHTML = 'Sign in <span>→</span>';
    }
  });
});

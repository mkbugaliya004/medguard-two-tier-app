
document.addEventListener("DOMContentLoaded", () => {
    console.log("MedGuard frontend loaded.");

    const appTitle = document.querySelector("#app-title");

    if (appTitle) {
        appTitle.textContent = "MedGuard";
    }
});

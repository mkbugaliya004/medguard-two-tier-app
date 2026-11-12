
document.addEventListener("DOMContentLoaded", () => {
    const resultsColumn = document.querySelector(".results-column");

    if (!resultsColumn) {
        return;
    }

    createPatientDirectory(resultsColumn);
});


function createPatientDirectory(container) {
    const card = document.createElement("section");
    card.className = "card";
    card.id = "patient-directory";

    const kicker = document.createElement("p");
    kicker.className = "section-kicker";
    kicker.textContent = "04 / PATIENTS";

    const heading = document.createElement("h2");
    heading.textContent = "Synthetic patient directory";

    const description = document.createElement("p");
    description.className = "muted";
    description.textContent =
        "Browse synthetic patient profiles saved in the database.";

    const controls = document.createElement("div");
    controls.className = "form-actions";

    const refreshButton = document.createElement("button");
    refreshButton.type = "button";
    refreshButton.className = "button button-primary";
    refreshButton.textContent = "Refresh patient list";

    const message = document.createElement("p");
    message.id = "patient-directory-message";
    message.setAttribute("role", "status");
    message.setAttribute("aria-live", "polite");
    message.textContent = "Select refresh to load saved patients.";

    const list = document.createElement("div");
    list.id = "patient-directory-list";

    controls.appendChild(refreshButton);

    card.append(
        kicker,
        heading,
        description,
        controls,
        message,
        list
    );

    container.appendChild(card);

    refreshButton.addEventListener("click", async () => {
        refreshButton.disabled = true;
        refreshButton.textContent = "Loading…";
        message.textContent = "Loading synthetic patient records…";
        list.replaceChildren();

        try {
            const patients = await getPatients();

            if (!Array.isArray(patients) || patients.length === 0) {
                message.textContent = "No synthetic patients have been saved yet.";
                return;
            }

            message.textContent =
                `${patients.length} patient record(s) retrieved.`;

            patients.forEach((patient) => {
                list.appendChild(createPatientCard(patient));
            });
        } catch (error) {
            console.error("Patient directory error:", error);
            message.textContent =
                error.message || "Unable to load patient records.";
        } finally {
            refreshButton.disabled = false;
            refreshButton.textContent = "Refresh patient list";
        }
    });
}


function createPatientCard(patient) {
    const item = document.createElement("article");
    item.className = "result-alert";

    const heading = document.createElement("h3");
    heading.textContent = `Patient ID: ${patient.patient_id}`;

    const medicine = document.createElement("p");
    medicine.textContent =
        `Medicine: ${patient.medicine || "Not recorded"}`;

    const age = document.createElement("p");
    age.textContent =
        `Age: ${patient.age ?? "Not recorded"}`;

    const diagnosis = document.createElement("p");
    diagnosis.textContent =
        `Cardiac diagnosis: ${patient.cardiac_diagnosis || "Not recorded"}`;

    const dose = document.createElement("p");
    dose.textContent =
        `Dose: ${patient.dose_mg ?? "Not recorded"} mg`;

    const historyButton = document.createElement("button");
    historyButton.type = "button";
    historyButton.className = "button button-secondary";
    historyButton.textContent = "View assessment history";

    historyButton.addEventListener("click", () => {
        const historyInput = document.querySelector("#history-patient-id");

        if (historyInput) {
            historyInput.value = patient.patient_id;

            document.querySelector("#assessment-history")
                ?.scrollIntoView({ behavior: "smooth" });

            document.querySelector("#assessment-history button")
                ?.click();
        }
    });

    item.append(
        heading,
        medicine,
        age,
        diagnosis,
        dose,
        historyButton
    );

    return item;
}

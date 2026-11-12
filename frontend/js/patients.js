
let allPatients = [];

document.addEventListener("DOMContentLoaded", () => {
    const container = document.querySelector(".directory-container");

    if (!container) {
        console.error("Patient directory container not found.");
        return;
    }

    createPatientDirectory(container);
    refreshPatientDirectory();
});


function createPatientDirectory(container) {
    const card = document.createElement("section");
    card.className = "card";
    card.id = "patient-directory";

    const heading = document.createElement("h2");
    heading.textContent = "Patient records";

    const description = document.createElement("p");
    description.className = "muted";
    description.textContent =
        "Search and browse synthetic patient profiles saved in MedGuard.";

    const controls = document.createElement("div");
    controls.className = "patient-controls";

    const search = document.createElement("input");
    search.type = "search";
    search.id = "patient-search";
    search.placeholder = "Search patient ID, medicine or diagnosis...";
    search.setAttribute("aria-label", "Search synthetic patients");

    const refreshButton = document.createElement("button");
    refreshButton.type = "button";
    refreshButton.className = "button button-primary";
    refreshButton.textContent = "↻ Refresh";

    const message = document.createElement("p");
    message.id = "patient-directory-message";
    message.setAttribute("role", "status");
    message.setAttribute("aria-live", "polite");
    message.textContent = "Loading synthetic patient records...";

    const list = document.createElement("div");
    list.id = "patient-directory-list";

    controls.append(search, refreshButton);

    card.append(
        heading,
        description,
        controls,
        message,
        list
    );

    container.appendChild(card);

    search.addEventListener("input", () => {
        renderPatientDirectory(search.value);
    });

    refreshButton.addEventListener("click", () => {
        refreshPatientDirectory();
    });
}


async function refreshPatientDirectory() {
    const message = document.querySelector("#patient-directory-message");
    const list = document.querySelector("#patient-directory-list");
    const refreshButton = document.querySelector(
        "#patient-directory button[type='button']"
    );

    if (!message || !list) return;

    if (refreshButton) {
        refreshButton.disabled = true;
        refreshButton.textContent = "Loading...";
    }

    message.textContent = "Retrieving patient records...";
    list.replaceChildren();

    try {
        const patients = await getPatients();

        if (!Array.isArray(patients)) {
            throw new Error("Unexpected patient directory response.");
        }

        allPatients = patients;

        updatePatientCount(allPatients.length);
        renderPatientDirectory(
            document.querySelector("#patient-search")?.value || ""
        );

        if (allPatients.length === 0) {
            message.textContent =
                "No synthetic patients have been saved yet.";
        } else {
            message.textContent =
                `${allPatients.length} synthetic patient record(s) found.`;
        }

    } catch (error) {
        console.error("Patient directory error:", error);

        message.textContent =
            error.message || "Unable to load patient records.";

        updatePatientCount(null);

    } finally {
        if (refreshButton) {
            refreshButton.disabled = false;
            refreshButton.textContent = "↻ Refresh";
        }
    }
}


function updatePatientCount(count) {
    const element = document.querySelector("#total-patients");

    if (!element) return;

    element.textContent =
        count === null || count === undefined
            ? "—"
            : String(count);
}


function renderPatientDirectory(searchTerm = "") {
    const list = document.querySelector("#patient-directory-list");
    const message = document.querySelector("#patient-directory-message");

    if (!list || !message) return;

    list.replaceChildren();

    const term = searchTerm.trim().toLowerCase();

    const filteredPatients = allPatients.filter((patient) => {
        const searchableText = [
            patient.patient_id,
            patient.medicine,
            patient.cardiac_diagnosis,
            patient.age,
            patient.dose_mg
        ]
            .filter((value) => value !== null && value !== undefined)
            .join(" ")
            .toLowerCase();

        return searchableText.includes(term);
    });

    if (allPatients.length === 0) {
        message.textContent = "No synthetic patient records are available.";
        return;
    }

    if (filteredPatients.length === 0) {
        message.textContent = "No patients match your search.";
        return;
    }

    message.textContent =
        `Showing ${filteredPatients.length} of ${allPatients.length} patient record(s).`;

    filteredPatients.forEach((patient) => {
        list.appendChild(createPatientCard(patient));
    });
}


function createPatientCard(patient) {
    const item = document.createElement("article");
    item.className = "patient-card";

    const top = document.createElement("div");
    top.className = "patient-card-top";

    const avatar = document.createElement("div");
    avatar.className = "patient-avatar";
    avatar.textContent = "♙";

    const identity = document.createElement("div");

    const heading = document.createElement("h3");
    heading.textContent = patient.patient_id || "Unknown ID";

    const medicine = document.createElement("span");
    medicine.className = "patient-medicine";
    medicine.textContent = formatMedicine(patient.medicine);

    identity.append(heading, medicine);
    top.append(avatar, identity);

    const details = document.createElement("div");
    details.className = "patient-details";

    addPatientDetail(details, "Age", patient.age ?? "Not recorded");
    addPatientDetail(
        details,
        "Diagnosis",
        patient.cardiac_diagnosis || "Not recorded"
    );
    addPatientDetail(
        details,
        "Dose",
        patient.dose_mg !== null && patient.dose_mg !== undefined
            ? `${patient.dose_mg} mg`
            : "Not recorded"
    );

    const historyButton = document.createElement("button");
    historyButton.type = "button";
    historyButton.className = "button button-secondary";
    historyButton.textContent = "View assessment history →";

    historyButton.addEventListener("click", () => {
        openPatientHistory(patient.patient_id);
    });

    item.append(top, details, historyButton);

    return item;
}


function addPatientDetail(container, label, value) {
    const row = document.createElement("div");
    row.className = "patient-detail-row";

    const labelElement = document.createElement("span");
    labelElement.textContent = label;

    const valueElement = document.createElement("strong");
    valueElement.textContent = String(value);

    row.append(labelElement, valueElement);
    container.appendChild(row);
}


function formatMedicine(value) {
    if (!value) return "Medicine not recorded";

    return value.charAt(0).toUpperCase() + value.slice(1);
}


function openPatientHistory(patientId) {
    const historyInput = document.querySelector("#history-patient-id");
    const historyButton = document.querySelector(
        "#assessment-history button"
    );

    if (!historyInput || !historyButton) {
        console.error("Assessment history panel is unavailable.");
        return;
    }

    historyInput.value = patientId;

    document.querySelector("#history")?.scrollIntoView({
        behavior: "smooth"
    });

    historyButton.click();
}

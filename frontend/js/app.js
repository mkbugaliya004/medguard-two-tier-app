
document.addEventListener("DOMContentLoaded", () => {
    const form = document.querySelector("#assessment-form");
    const result = document.querySelector("#assessment-result");
    const submitButton = form?.querySelector('button[type="submit"]');

    if (!form || !result || !submitButton) {
        console.error("MedGuard assessment form elements were not found.");
        return;
    }

    createHistoryPanel();

    const defaultButtonText = submitButton.textContent.trim();

    form.addEventListener("submit", async (event) => {
        event.preventDefault();

        const formData = new FormData(form);

        const patientData = {
            patient_id: String(formData.get("patient_id") || "").trim(),
            medicine: formData.get("medicine"),
            cardiac_diagnosis:
                String(formData.get("cardiac_diagnosis") || "").trim() || null
        };

        const numericFields = [
            "age",
            "dose_mg",
            "heart_rate",
            "qtc_ms",
            "qrs_ms",
            "baseline_qrs_ms",
            "crcl",
            "lvef_percent",
            "potassium",
            "magnesium"
        ];

        const booleanFields = [
            "thyroid_tests_overdue",
            "liver_function_abnormal",
            "thyroid_function_abnormal",
            "multiple_rate_limiting_medicines",
            "structural_heart_disease",
            "long_qt_syndrome",
            "qt_prolonging_interaction",
            "bradycardia_symptoms"
        ];

        numericFields.forEach((field) => {
            patientData[field] = readNumber(formData, field);
        });

        booleanFields.forEach((field) => {
            patientData[field] = formData.get(field) === "true";
        });

        const validation = validateAssessment(patientData);

        if (!patientData.patient_id) {
            validation.errors.unshift("Synthetic Patient ID is required.");
            validation.valid = false;
        } else if (
            patientData.patient_id.length > 50 ||
            !/^[A-Za-z0-9_-]+$/.test(patientData.patient_id)
        ) {
            validation.errors.unshift(
                "Patient ID can contain only letters, numbers, hyphens and underscores, up to 50 characters."
            );
            validation.valid = false;
        }

        if (!validation.valid) {
            showMessage(result, validation.errors.join(" "));
            return;
        }

        submitButton.disabled = true;
        submitButton.textContent = "Assessing profile…";

        showMessage(result, "Processing synthetic patient assessment…");

        try {
            const assessment = await assessMedication(patientData);

            displayAssessment(assessment, result);
            updateLatestAssessment(assessment);

            await loadPatientHistory(patientData.patient_id);

            // Refresh the directory and dashboard patient count.
            if (typeof refreshPatientDirectory === "function") {
                await refreshPatientDirectory();
            }
        } catch (error) {
            console.error("MedGuard assessment error:", error);

            showMessage(
                result,
                error.message || "Assessment failed. Check the API connection and try again."
            );
        } finally {
            submitButton.disabled = false;
            submitButton.textContent = defaultButtonText;
        }
    });

    form.addEventListener("reset", () => {
        window.setTimeout(() => {
            result.replaceChildren();

            const emptyState = document.createElement("div");
            emptyState.className = "empty-state";

            const heading = document.createElement("h3");
            heading.textContent = "Ready for assessment";

            const message = document.createElement("p");
            message.textContent =
                "Complete a synthetic profile and run an assessment to view the results.";

            emptyState.append(heading, message);
            result.appendChild(emptyState);
        }, 0);
    });
});


function readNumber(formData, fieldName) {
    const value = formData.get(fieldName);

    if (value === null || String(value).trim() === "") {
        return null;
    }

    return Number(value);
}


function showMessage(container, message) {
    container.replaceChildren();

    const paragraph = document.createElement("p");
    paragraph.textContent = message;

    container.appendChild(paragraph);
}


function updateLatestAssessment(assessment) {
    const element = document.querySelector("#latest-assessment");

    if (!element) return;

    if (assessment.created_at) {
        element.textContent = formatDate(assessment.created_at);
    } else {
        element.textContent = "Completed";
    }
}


function displayAssessment(assessment, result) {
    result.replaceChildren();

    const heading = document.createElement("h3");
    heading.textContent = "Assessment summary";
    result.appendChild(heading);

    const patient = document.createElement("p");
    patient.textContent = `Patient ID: ${assessment.patient_id}`;
    result.appendChild(patient);

    const medicine = document.createElement("p");
    medicine.textContent = `Medicine: ${assessment.medicine}`;
    result.appendChild(medicine);

    const count = document.createElement("p");
    count.textContent = `Alerts generated: ${assessment.alert_count}`;
    result.appendChild(count);

    const status = document.createElement("div");
    status.className = "result-status";

    status.textContent =
        assessment.status === "alerts_found"
            ? "Review required: alerts were generated"
            : "No alerts generated by the current rules";

    result.appendChild(status);

    if (assessment.assessment_id !== undefined) {
        const reference = document.createElement("p");
        reference.textContent =
            `Assessment reference: ${assessment.assessment_id}`;
        result.appendChild(reference);
    }

    if (Array.isArray(assessment.alerts) && assessment.alerts.length > 0) {
        const alertsHeading = document.createElement("h3");
        alertsHeading.textContent = "Generated safety alerts";
        result.appendChild(alertsHeading);

        assessment.alerts.forEach((alert) => {
            const severity = ["high", "review"].includes(
                String(alert.severity).toLowerCase()
            )
                ? String(alert.severity).toLowerCase()
                : "";

            const alertCard = document.createElement("article");
            alertCard.className = `result-alert ${severity}`.trim();

            const alertHeading = document.createElement("h3");
            alertHeading.textContent =
                `${alert.code || "Alert"} — ${alert.severity || "Unspecified severity"}`;

            const alertMessage = document.createElement("p");
            alertMessage.textContent =
                alert.message || "No alert description provided.";

            alertCard.append(alertHeading, alertMessage);
            result.appendChild(alertCard);
        });
    } else {
        const noAlerts = document.createElement("p");
        noAlerts.textContent =
            "No alerts were generated by the current draft rules. This does not mean the medicine is safe.";

        result.appendChild(noAlerts);
    }

    if (assessment.educational_warning) {
        const warning = document.createElement("p");
        warning.className = "results-footnote";
        warning.textContent = assessment.educational_warning;
        result.appendChild(warning);
    }
}


function createHistoryPanel() {
    const container = document.querySelector(".history-container");

    if (!container) return;

    const card = document.createElement("section");
    card.className = "card";
    card.id = "assessment-history";

    const field = document.createElement("div");
    field.className = "field";

    const label = document.createElement("label");
    label.htmlFor = "history-patient-id";
    label.textContent = "Synthetic patient ID";

    const input = document.createElement("input");
    input.id = "history-patient-id";
    input.type = "text";
    input.maxLength = 50;
    input.placeholder = "e.g. SYN-001";

    const button = document.createElement("button");
    button.type = "button";
    button.className = "button button-primary";
    button.textContent = "Load assessment history";

    const message = document.createElement("p");
    message.id = "history-message";
    message.setAttribute("role", "status");
    message.setAttribute("aria-live", "polite");
    message.textContent = "Enter a patient ID to retrieve saved assessments.";

    const list = document.createElement("div");
    list.id = "history-list";

    field.append(label, input);

    card.append(
        field,
        button,
        message,
        list
    );

    container.appendChild(card);

    const patientIdInput = document.querySelector("#patient-id");

    patientIdInput?.addEventListener("input", () => {
        input.value = patientIdInput.value;
    });

    button.addEventListener("click", async () => {
        const patientId = input.value.trim();

        if (
            !patientId ||
            patientId.length > 50 ||
            !/^[A-Za-z0-9_-]+$/.test(patientId)
        ) {
            message.textContent = "Enter a valid synthetic patient ID.";
            list.replaceChildren();
            return;
        }

        button.disabled = true;
        button.textContent = "Loading…";

        try {
            await loadPatientHistory(patientId);
        } finally {
            button.disabled = false;
            button.textContent = "Load assessment history";
        }
    });
}


async function loadPatientHistory(patientId) {
    const message = document.querySelector("#history-message");
    const list = document.querySelector("#history-list");

    if (!message || !list) return;

    message.textContent = "Retrieving saved assessments…";
    list.replaceChildren();

    try {
        const history = await getPatientAssessmentHistory(patientId);

        if (!Array.isArray(history) || history.length === 0) {
            message.textContent =
                "No saved assessments were found for this patient.";
            return;
        }

        message.textContent =
            `${history.length} saved assessment(s) found for ${patientId}.`;

        history.forEach((record) => {
            const item = document.createElement("article");
            item.className = "result-alert";

            const heading = document.createElement("h3");
            heading.textContent =
                `Assessment #${record.id} — ${record.medicine}`;

            const status = document.createElement("p");
            status.textContent =
                `Status: ${record.status} | Alerts: ${record.alert_count}`;

            const date = document.createElement("p");
            date.textContent = `Created: ${formatDate(record.created_at)}`;

            item.append(heading, status, date);

            if (Array.isArray(record.alerts) && record.alerts.length > 0) {
                record.alerts.forEach((alert) => {
                    const alertDetail = document.createElement("p");
                    alertDetail.textContent =
                        `${alert.code || "Alert"}: ${alert.message || "No description"}`;
                    item.appendChild(alertDetail);
                });
            }

            list.appendChild(item);
        });
    } catch (error) {
        console.error("History retrieval error:", error);
        message.textContent =
            error.message || "Unable to retrieve assessment history.";
    }
}


function formatDate(value) {
    if (!value) return "Date not available";

    const date = new Date(value);

    if (Number.isNaN(date.getTime())) {
        return "Date not available";
    }

    return date.toLocaleString();
}

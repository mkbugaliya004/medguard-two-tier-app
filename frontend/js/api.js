
const API_BASE_URL = "/api/v1";

async function assessMedication(patientData) {
    const response = await fetch(`${API_BASE_URL}/assessments`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(patientData)
    });

    if (!response.ok) {
        let message = "Medication assessment failed.";

        try {
            const errorData = await response.json();
            message = errorData.detail
                ? JSON.stringify(errorData.detail)
                : message;
        } catch {
            // Keep the default error message.
        }

        throw new Error(message);
    }

    return response.json();
}

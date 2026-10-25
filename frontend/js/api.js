
const API_BASE_URL = "/api/v1";

async function assessMedication(patientData) {
    const response = await fetch(
        `${API_BASE_URL}/assessments`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(patientData)
        }
    );

    if (!response.ok) {
        throw new Error("Medication assessment failed.");
    }

    return response.json();
}

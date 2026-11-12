
const API_BASE_URL = "/api/v1";


async function handleApiResponse(response, defaultMessage) {
    if (!response.ok) {
        let message = defaultMessage;

        try {
            const errorData = await response.json();
            message = errorData.detail || message;
        } catch {
            // Keep the default error message.
        }

        throw new Error(message);
    }

    return await response.json();
}


async function assessMedication(patientData) {
    const response = await fetch(`${API_BASE_URL}/assessments/`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(patientData)
    });

    return handleApiResponse(
        response,
        "Assessment request failed."
    );
}


async function getPatientAssessmentHistory(patientId) {
    const safePatientId = encodeURIComponent(patientId);

    const response = await fetch(
        `${API_BASE_URL}/assessments/patient/${safePatientId}`
    );

    return handleApiResponse(
        response,
        "Unable to retrieve patient assessment history."
    );
}

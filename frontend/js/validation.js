
function validateAssessment(data) {
    const errors = [];

    const supportedMedicines = [
        "sotalol",
        "flecainide",
        "amiodarone"
    ];

    if (!supportedMedicines.includes(data.medicine)) {
        errors.push("Please select a supported medicine.");
    }

    const numericLimits = {
        age: [0, 120],
        heart_rate: [0, 300],
        qtc_ms: [0, 1000],
        qrs_ms: [0, 500],
        potassium: [0, 15],
        magnesium: [0, 10],
        crcl: [0, 300]
    };

    for (const [field, limits] of Object.entries(numericLimits)) {
        const value = data[field];

        if (value === null || value === undefined) {
            continue;
        }

        if (
            typeof value !== "number" ||
            !Number.isFinite(value) ||
            value < limits[0] ||
            value > limits[1]
        ) {
            errors.push(`${field} must be between ${limits[0]} and ${limits[1]}.`);
        }
    }

    return {
        valid: errors.length === 0,
        errors
    };
}


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

    if (
        data.qtc_ms != null &&
        (!Number.isFinite(data.qtc_ms) || data.qtc_ms < 0)
    ) {
        errors.push("QTc must be a valid non-negative number.");
    }

    if (
        data.heart_rate != null &&
        (!Number.isFinite(data.heart_rate) ||
         data.heart_rate < 0)
    ) {
        errors.push("Heart rate must be a valid non-negative number.");
    }

    return {
        valid: errors.length === 0,
        errors
    };
}

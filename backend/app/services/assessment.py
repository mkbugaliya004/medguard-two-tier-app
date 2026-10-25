
from app.schemas.patient import PatientProfile


def assess_medication(profile: PatientProfile) -> dict:
    """
    Coordinate a medication safety assessment.

    This is an initial placeholder. Medicine-specific
    safety rules will be implemented separately.
    """
    return {
        "medicine": profile.medicine,
        "status": "not_assessed",
        "alerts": [],
        "message": (
            "Assessment service created. "
            "Medication safety rules are not implemented yet."
        ),
        "educational_warning": (
            "Synthetic data only. Not for clinical decision-making."
        ),
    }

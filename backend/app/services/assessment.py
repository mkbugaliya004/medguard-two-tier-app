
"""Coordinate medicine-specific safety assessments."""

from app.schemas.patient import PatientProfile
from app.rules.sotalol import check_sotalol
from app.rules.flecainide import check_flecainide
from app.rules.amiodarone import check_amiodarone


def assess_medication(profile: PatientProfile) -> dict:
    """Run the draft rules for the selected medicine."""

    rule_checks = {
        "sotalol": check_sotalol,
        "flecainide": check_flecainide,
        "amiodarone": check_amiodarone,
    }

    alerts = rule_checks[profile.medicine](profile)

    return {
        "medicine": profile.medicine,
        "status": "alerts_found" if alerts else "no_alerts_generated",
        "alert_count": len(alerts),
        "alerts": alerts,
        "educational_warning": (
            "Synthetic data only. This educational prototype is "
            "not for clinical decision-making."
        ),
    }


"""Draft Flecainide safety rules for synthetic profiles.

Educational prototype only. Rules require authoritative
reference checks and supervisor review.
"""


def check_flecainide(profile) -> list[dict]:
    """Return draft safety alerts for a synthetic patient profile."""
    alerts = []

    if (
        profile.structural_heart_disease
        or profile.ischaemic_heart_disease
        or profile.reduced_lvef
    ):
        alerts.append({
            "code": "FLE-001",
            "severity": "high",
            "message": (
                "Structural or ischaemic heart disease, or reduced LVEF, "
                "requires specialist review before Flecainide use."
            ),
        })

    if profile.qrs_ms is not None and profile.qrs_ms >= 120:
        alerts.append({
            "code": "FLE-002",
            "severity": "review",
            "message": (
                "QRS duration is prolonged; review the ECG and "
                "relevant clinical guidance."
            ),
        })

    if profile.conduction_disease or profile.conduction_abnormality:
        alerts.append({
            "code": "FLE-003",
            "severity": "high",
            "message": (
                "Conduction disease or abnormality requires "
                "specialist review."
            ),
        })

    if profile.brugada_syndrome:
        alerts.append({
            "code": "FLE-004",
            "severity": "high",
            "message": "Brugada syndrome requires specialist review."

        })

    return alerts

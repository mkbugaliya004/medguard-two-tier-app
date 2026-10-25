
"""Draft Sotalol safety rules for synthetic profiles.

Educational prototype only. Thresholds and rules require
verification against authoritative guidance and supervisor review.
"""


def check_sotalol(profile) -> list[dict]:
    """Return draft safety alerts for a synthetic patient profile."""
    alerts = []

    if profile.qtc_ms is not None and profile.qtc_ms >= 500:
        alerts.append({
            "code": "SOT-001",
            "severity": "high",
            "message": "QTc is 500 ms or above; urgent clinical review is indicated.",
        })

    if profile.potassium is not None and profile.potassium < 3.5:
        alerts.append({
            "code": "SOT-002",
            "severity": "high",
            "message": "Potassium is below the draft safety threshold; review is required.",
        })

    if profile.magnesium is not None and profile.magnesium < 0.7:
        alerts.append({
            "code": "SOT-003",
            "severity": "review",
            "message": "Magnesium is below the draft threshold; review is required.",
        })

    if profile.crcl is not None and profile.crcl < 60:
        alerts.append({
            "code": "SOT-004",
            "severity": "review",
            "message": "Renal function requires review for Sotalol dosing and safety.",
        })

    if profile.long_qt_syndrome:
        alerts.append({
            "code": "SOT-005",
            "severity": "high",
            "message": "History of long-QT syndrome requires specialist review.",
        })

    if profile.qt_prolonging_interaction:
        alerts.append({
            "code": "SOT-006",
            "severity": "high",
            "message": "Potential interaction with another QT-prolonging medicine requires review.",
        })

    return alerts


"""Draft Amiodarone safety rules for synthetic profiles.

Educational prototype only. Monitoring rules require
verification against authoritative guidance and supervisor review.
"""

from datetime import date


def check_amiodarone(profile) -> list[dict]:
    """Return draft safety alerts for a synthetic patient profile."""
    alerts = []

    if profile.heart_rate is not None and profile.heart_rate <= 50:
        alerts.append({
            "code": "AMI-001",
            "severity": "high",
            "message": (
                "Heart rate is 50 bpm or below; clinical review "
                "is required."
            ),
        })

    if profile.liver_function_abnormal:
        alerts.append({
            "code": "AMI-002",
            "severity": "review",
            "message": (
                "Abnormal liver function is recorded; review liver "
                "tests and the monitoring plan."
            ),
        })

    if profile.thyroid_function_abnormal:
        alerts.append({
            "code": "AMI-003",
            "severity": "review",
            "message": (
                "Abnormal thyroid function is recorded; review "
                "the results and monitoring plan."
            ),
        })

    if profile.thyroid_tests_overdue:
        alerts.append({
            "code": "AMI-004",
            "severity": "review",
            "message": (
                "Thyroid monitoring is marked overdue; arrange "
                "review according to the monitoring protocol."
            ),
        })

    today = date.today()

    if profile.last_thyroid_test_date is None:
        alerts.append({
            "code": "AMI-005",
            "severity": "review",
            "message": "No previous thyroid test date is recorded.",
        })
    elif (today - profile.last_thyroid_test_date).days > 183:
        alerts.append({
            "code": "AMI-006",
            "severity": "review",
            "message": (
                "The last recorded thyroid test was over six months "
                "ago; review whether monitoring is due."
            ),
        })

    if profile.last_liver_test_date is None:
        alerts.append({
            "code": "AMI-007",
            "severity": "review",
            "message": "No previous liver test date is recorded.",
        })

    if profile.pulmonary_symptoms:
        alerts.append({
            "code": "AMI-008",
            "severity": "high",
            "message": (
                "Pulmonary symptoms are reported; prompt clinical "
                "assessment is required."
            ),
        })

    if profile.vision_concerns:
        alerts.append({
            "code": "AMI-009",
            "severity": "review",
            "message": "Vision concerns are recorded; clinical review is required.",
        })

    return alerts

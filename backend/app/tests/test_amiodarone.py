
from app.schemas.patient import PatientProfile
from app.services.assessment import assess_medication


def test_amiodarone_overdue_thyroid_monitoring_generates_alert():
    profile = PatientProfile(
        medicine="amiodarone",
        thyroid_tests_overdue=True,
    )

    result = assess_medication(profile)

    assert result["medicine"] == "amiodarone"
    assert result["alert_count"] >= 1
    assert any(
        alert["code"] == "AMI-004"
        for alert in result["alerts"]
    )

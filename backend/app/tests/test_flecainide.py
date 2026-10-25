
from app.schemas.patient import PatientProfile
from app.services.assessment import assess_medication


def test_flecainide_structural_heart_disease_generates_alert():
    profile = PatientProfile(
        medicine="flecainide",
        structural_heart_disease=True,
    )

    result = assess_medication(profile)

    assert result["medicine"] == "flecainide"
    assert result["alert_count"] >= 1
    assert any(
        alert["code"] == "FLE-001"
        for alert in result["alerts"]
    )

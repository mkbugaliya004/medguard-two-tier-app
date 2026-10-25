
from app.schemas.patient import PatientProfile
from app.services.assessment import assess_medication


def test_sotalol_high_qtc_generates_alert():
    profile = PatientProfile(
        medicine="sotalol",
        qtc_ms=520,
    )

    result = assess_medication(profile)

    assert result["medicine"] == "sotalol"
    assert result["alert_count"] >= 1
    assert any(
        alert["code"] == "SOT-001"
        for alert in result["alerts"]
    )

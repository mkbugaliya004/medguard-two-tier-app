
def test_assessment_is_saved_to_database(client):
    payload = {
        "patient_id": "SYN-TEST-001",
        "medicine": "sotalol",
        "qtc_ms": 520,
    }

    response = client.post(
        "/api/v1/assessments/",
        json=payload,
    )

    assert response.status_code == 200

    result = response.json()

    assert result["patient_id"] == "SYN-TEST-001"
    assert result["medicine"] == "sotalol"
    assert result["alert_count"] >= 1
    assert result["assessment_id"] is not None


def test_assessment_history_is_retrievable(client):
    payload = {
        "patient_id": "SYN-TEST-002",
        "medicine": "amiodarone",
        "thyroid_tests_overdue": True,
    }

    create_response = client.post(
        "/api/v1/assessments/",
        json=payload,
    )

    assert create_response.status_code == 200

    history_response = client.get(
        "/api/v1/assessments/patient/SYN-TEST-002"
    )

    assert history_response.status_code == 200

    history = history_response.json()

    assert len(history) == 1
    assert history[0]["medicine"] == "amiodarone"
    assert history[0]["alert_count"] >= 1


def test_unknown_patient_history_returns_404(client):
    response = client.get(
        "/api/v1/assessments/patient/UNKNOWN-001"
    )

    assert response.status_code == 404

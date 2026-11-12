
def test_create_patient(client):
    payload = {
        "patient_id": "SYN-PAT-001",
        "medicine": "sotalol",
        "qtc_ms": 480,
    }

    response = client.post(
        "/api/v1/patients/",
        json=payload,
    )

    assert response.status_code == 200
    assert response.json()["patient_id"] == "SYN-PAT-001"


def test_get_patient_by_id(client):
    payload = {
        "patient_id": "SYN-PAT-002",
        "medicine": "flecainide",
    }

    client.post("/api/v1/patients/", json=payload)

    response = client.get(
        "/api/v1/patients/SYN-PAT-002"
    )

    assert response.status_code == 200
    assert response.json()["medicine"] == "flecainide"


def test_list_patients(client):
    payload = {
        "patient_id": "SYN-PAT-003",
        "medicine": "amiodarone",
    }

    client.post("/api/v1/patients/", json=payload)

    response = client.get("/api/v1/patients/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_duplicate_patient_id_returns_409(client):
    payload = {
        "patient_id": "SYN-PAT-004",
        "medicine": "sotalol",
    }

    first_response = client.post(
        "/api/v1/patients/",
        json=payload,
    )

    second_response = client.post(
        "/api/v1/patients/",
        json=payload,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 409


def test_list_patients_rejects_negative_skip(client):
    response = client.get(
        "/api/v1/patients/?skip=-1"
    )

    assert response.status_code == 422


def test_list_patients_rejects_limit_above_100(client):
    response = client.get(
        "/api/v1/patients/?limit=101"
    )

    assert response.status_code == 422

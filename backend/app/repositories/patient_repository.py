
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientProfile


def get_patient(db: Session, patient_id: str):
    return db.query(Patient).filter(
        Patient.patient_id == patient_id
    ).first()


def create_patient(
    db: Session,
    profile: PatientProfile,
    commit: bool = True,
):
    patient = Patient(**profile.model_dump())

    db.add(patient)

    if commit:
        db.commit()
    else:
        db.flush()

    db.refresh(patient)

    return patient


def update_patient(
    db: Session,
    patient_id: str,
    profile: PatientProfile,
    commit: bool = True,
):
    patient = get_patient(db, patient_id)

    if not patient:
        return None

    for field, value in profile.model_dump().items():
        setattr(patient, field, value)

    if commit:
        db.commit()
    else:
        db.flush()

    db.refresh(patient)

    return patient


def get_all_patients(
    db: Session,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Patient)
        .offset(skip)
        .limit(limit)
        .all()
    )

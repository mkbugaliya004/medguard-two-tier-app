
from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.schemas.patient import PatientProfile


def get_patient(db: Session, patient_id: str):
    return db.query(Patient).filter(
        Patient.patient_id == patient_id
    ).first()


def create_patient(db: Session, profile: PatientProfile):
    patient = Patient(**profile.model_dump())

    db.add(patient)
    db.commit()
    db.refresh(patient)

    return patient


def get_all_patients(db: Session, skip: int = 0, limit: int = 100):
    return (
        db.query(Patient)
        .offset(skip)
        .limit(limit)
        .all()
    )

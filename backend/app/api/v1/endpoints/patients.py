
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import patient_repository
from app.schemas.patient import PatientProfile


router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("/")
def create_patient(
    profile: PatientProfile,
    db: Session = Depends(get_db),
):
    existing_patient = patient_repository.get_patient(
        db, profile.patient_id
    )

    if existing_patient:
        raise HTTPException(
            status_code=409,
            detail="Patient ID already exists",
        )

    return patient_repository.create_patient(db, profile)


@router.get("/{patient_id}")
def get_patient(
    patient_id: str,
    db: Session = Depends(get_db),
):
    patient = patient_repository.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return patient


@router.get("/")
def get_patients(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return patient_repository.get_all_patients(
        db, skip=skip, limit=limit
    )

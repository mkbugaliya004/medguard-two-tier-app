
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import assessment_repository, patient_repository
from app.schemas.patient import PatientProfile
from app.services.assessment import assess_medication


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.post("/")
def create_patient_assessment(
    profile: PatientProfile,
    db: Session = Depends(get_db),
):
    patient = patient_repository.get_patient(
        db, profile.patient_id
    )

    if patient:
        patient_repository.update_patient(
            db, profile.patient_id, profile
        )
    else:
        patient_repository.create_patient(db, profile)

    result = assess_medication(profile)

    saved_assessment = assessment_repository.create_assessment(
        db=db,
        patient_id=profile.patient_id,
        medicine=result["medicine"],
        status=result["status"],
        alert_count=result["alert_count"],
        alerts=result["alerts"],
    )

    return {
        "assessment_id": saved_assessment.id,
        "patient_id": profile.patient_id,
        "medicine": result["medicine"],
        "status": result["status"],
        "alert_count": result["alert_count"],
        "alerts": result["alerts"],
        "created_at": saved_assessment.created_at,
        "educational_warning": result["educational_warning"],
    }


@router.get("/patient/{patient_id}")
def get_patient_assessment_history(
    patient_id: str,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1, le=100),
    db: Session = Depends(get_db),
):
    patient = patient_repository.get_patient(db, patient_id)

    if not patient:
        raise HTTPException(
            status_code=404,
            detail="Patient not found",
        )

    return assessment_repository.get_patient_assessments(
        db,
        patient_id=patient_id,
        skip=skip,
        limit=limit,
    )

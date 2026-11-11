
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories import assessment_repository, patient_repository


router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)


@router.get("/patient/{patient_id}")
def get_patient_assessment_history(
    patient_id: str,
    skip: int = 0,
    limit: int = 100,
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

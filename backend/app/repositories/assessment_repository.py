
from sqlalchemy.orm import Session

from app.models.assessment import Assessment


def create_assessment(
    db: Session,
    patient_id: str,
    medicine: str,
    status: str,
    alert_count: int,
    alerts: list,
    commit: bool = True,
):
    assessment = Assessment(
        patient_id=patient_id,
        medicine=medicine,
        status=status,
        alert_count=alert_count,
        alerts=alerts,
    )

    db.add(assessment)

    if commit:
        db.commit()
    else:
        db.flush()

    db.refresh(assessment)

    return assessment


def get_patient_assessments(
    db: Session,
    patient_id: str,
    skip: int = 0,
    limit: int = 100,
):
    return (
        db.query(Assessment)
        .filter(Assessment.patient_id == patient_id)
        .order_by(Assessment.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )

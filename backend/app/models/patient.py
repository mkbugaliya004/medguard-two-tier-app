
from datetime import date

from sqlalchemy import Boolean, Date, Float, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Patient(Base):
    __tablename__ = "patients"

    patient_id: Mapped[str] = mapped_column(String(50), primary_key=True)
    age: Mapped[int | None] = mapped_column(Integer, nullable=True)

    medicine: Mapped[str] = mapped_column(String(20), nullable=False)
    dose_mg: Mapped[float | None] = mapped_column(Float, nullable=True)
    other_medications: Mapped[list] = mapped_column(JSON, default=list)

    multiple_rate_limiting_medicines: Mapped[bool] = mapped_column(Boolean, default=False)
    qt_prolonging_interaction: Mapped[bool] = mapped_column(Boolean, default=False)

    cardiac_diagnosis: Mapped[str | None] = mapped_column(String(200), nullable=True)
    lvef_percent: Mapped[float | None] = mapped_column(Float, nullable=True)
    heart_rate: Mapped[int | None] = mapped_column(Integer, nullable=True)
    qtc_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    qrs_ms: Mapped[float | None] = mapped_column(Float, nullable=True)
    baseline_qrs_ms: Mapped[float | None] = mapped_column(Float, nullable=True)

    crcl: Mapped[float | None] = mapped_column(Float, nullable=True)
    potassium: Mapped[float | None] = mapped_column(Float, nullable=True)
    magnesium: Mapped[float | None] = mapped_column(Float, nullable=True)

    alt_u_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    ast_u_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    liver_uln_u_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    tsh_miu_l: Mapped[float | None] = mapped_column(Float, nullable=True)
    free_t4_pmol_l: Mapped[float | None] = mapped_column(Float, nullable=True)

    liver_function_abnormal: Mapped[bool] = mapped_column(Boolean, default=False)
    thyroid_function_abnormal: Mapped[bool] = mapped_column(Boolean, default=False)
    thyroid_tests_overdue: Mapped[bool] = mapped_column(Boolean, default=False)

    long_qt_syndrome: Mapped[bool] = mapped_column(Boolean, default=False)
    structural_heart_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    ischaemic_heart_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    uncontrolled_heart_failure: Mapped[bool] = mapped_column(Boolean, default=False)
    reduced_lvef: Mapped[bool] = mapped_column(Boolean, default=False)
    conduction_disease: Mapped[bool] = mapped_column(Boolean, default=False)
    brugada_syndrome: Mapped[bool] = mapped_column(Boolean, default=False)
    electrolyte_abnormality: Mapped[bool] = mapped_column(Boolean, default=False)
    bradycardia_symptoms: Mapped[bool] = mapped_column(Boolean, default=False)
    conduction_abnormality: Mapped[bool] = mapped_column(Boolean, default=False)
    pulmonary_symptoms: Mapped[bool] = mapped_column(Boolean, default=False)
    vision_concerns: Mapped[bool] = mapped_column(Boolean, default=False)

    last_ecg_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_thyroid_test_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    last_liver_test_date: Mapped[date | None] = mapped_column(Date, nullable=True)

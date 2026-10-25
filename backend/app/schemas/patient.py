
from datetime import date
from typing import Literal

from pydantic import BaseModel, Field


class PatientProfile(BaseModel):
    """Synthetic patient profile for educational safety assessment."""

    # Patient and medication details
    patient_id: str = Field(default="SYN-001", max_length=50)
    age: int | None = Field(default=None, ge=0, le=120)

    medicine: Literal["sotalol", "flecainide", "amiodarone"]
    dose_mg: float | None = Field(default=None, gt=0, le=5000)
    other_medications: list[str] = Field(default_factory=list)
    multiple_rate_limiting_medicines: bool = False
    qt_prolonging_interaction: bool = False

    # Cardiac history and measurements
    cardiac_diagnosis: str | None = Field(default=None, max_length=200)
    lvef_percent: float | None = Field(default=None, ge=0, le=100)
    heart_rate: int | None = Field(default=None, ge=0, le=300)
    qtc_ms: float | None = Field(default=None, ge=0, le=1000)
    qrs_ms: float | None = Field(default=None, ge=0, le=500)
    baseline_qrs_ms: float | None = Field(default=None, ge=0, le=500)

    # Renal function and electrolytes
    crcl: float | None = Field(default=None, ge=0, le=300)
    potassium: float | None = Field(default=None, ge=0, le=15)
    magnesium: float | None = Field(default=None, ge=0, le=10)

    # Liver and thyroid information
    alt_u_l: float | None = Field(default=None, ge=0)
    ast_u_l: float | None = Field(default=None, ge=0)
    liver_uln_u_l: float | None = Field(default=None, gt=0)
    tsh_miu_l: float | None = Field(default=None, ge=0)
    free_t4_pmol_l: float | None = Field(default=None, ge=0)

    liver_function_abnormal: bool = False
    thyroid_function_abnormal: bool = False
    thyroid_tests_overdue: bool = False

    # Relevant history
    long_qt_syndrome: bool = False
    structural_heart_disease: bool = False
    ischaemic_heart_disease: bool = False
    uncontrolled_heart_failure: bool = False
    reduced_lvef: bool = False
    conduction_disease: bool = False
    brugada_syndrome: bool = False
    electrolyte_abnormality: bool = False
    bradycardia_symptoms: bool = False
    conduction_abnormality: bool = False
    pulmonary_symptoms: bool = False
    vision_concerns: bool = False

    # Monitoring dates
    last_ecg_date: date | None = None
    last_thyroid_test_date: date | None = None
    last_liver_test_date: date | None = None

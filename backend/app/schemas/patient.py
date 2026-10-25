
from typing import Literal

from pydantic import BaseModel, Field


class PatientProfile(BaseModel):
    """Synthetic patient inputs for a medication safety assessment."""

    medicine: Literal["sotalol", "flecainide", "amiodarone"]

    qtc_ms: float | None = Field(default=None, ge=0, le=1000)
    heart_rate: int | None = Field(default=None, ge=0, le=300)

    qrs_ms: float | None = Field(default=None, ge=0, le=500)
    baseline_qrs_ms: float | None = Field(default=None, ge=0, le=500)

    crcl: float | None = Field(default=None, ge=0, le=300)
    potassium: float | None = Field(default=None, ge=0, le=15)
    magnesium: float | None = Field(default=None, ge=0, le=10)

    long_qt_syndrome: bool = False
    qt_prolonging_interaction: bool = False
    uncontrolled_heart_failure: bool = False

    structural_heart_disease: bool = False
    ischaemic_heart_disease: bool = False
    reduced_lvef: bool = False
    conduction_disease: bool = False
    brugada_syndrome: bool = False

    electrolyte_abnormality: bool = False
    bradycardia_symptoms: bool = False
    conduction_abnormality: bool = False

    thyroid_abnormal: bool = False
    thyroid_tests_overdue: bool = False
    pulmonary_symptoms: bool = False
    vision_concerns: bool = False
    liver_enzymes_elevated: bool = False

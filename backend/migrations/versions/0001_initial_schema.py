
"""Create initial MedGuard database schema."""

from alembic import op
import sqlalchemy as sa


revision = "0001_initial_schema"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "patients",
        sa.Column("patient_id", sa.String(length=50), primary_key=True),
        sa.Column("age", sa.Integer(), nullable=True),
        sa.Column("medicine", sa.String(length=20), nullable=False),
        sa.Column("dose_mg", sa.Float(), nullable=True),
        sa.Column("other_medications", sa.JSON(), nullable=False),
        sa.Column("multiple_rate_limiting_medicines", sa.Boolean(), nullable=False),
        sa.Column("qt_prolonging_interaction", sa.Boolean(), nullable=False),
        sa.Column("cardiac_diagnosis", sa.String(length=200), nullable=True),
        sa.Column("lvef_percent", sa.Float(), nullable=True),
        sa.Column("heart_rate", sa.Integer(), nullable=True),
        sa.Column("qtc_ms", sa.Float(), nullable=True),
        sa.Column("qrs_ms", sa.Float(), nullable=True),
        sa.Column("baseline_qrs_ms", sa.Float(), nullable=True),
        sa.Column("crcl", sa.Float(), nullable=True),
        sa.Column("potassium", sa.Float(), nullable=True),
        sa.Column("magnesium", sa.Float(), nullable=True),
        sa.Column("alt_u_l", sa.Float(), nullable=True),
        sa.Column("ast_u_l", sa.Float(), nullable=True),
        sa.Column("liver_uln_u_l", sa.Float(), nullable=True),
        sa.Column("tsh_miu_l", sa.Float(), nullable=True),
        sa.Column("free_t4_pmol_l", sa.Float(), nullable=True),
        sa.Column("liver_function_abnormal", sa.Boolean(), nullable=False),
        sa.Column("thyroid_function_abnormal", sa.Boolean(), nullable=False),
        sa.Column("thyroid_tests_overdue", sa.Boolean(), nullable=False),
        sa.Column("long_qt_syndrome", sa.Boolean(), nullable=False),
        sa.Column("structural_heart_disease", sa.Boolean(), nullable=False),
        sa.Column("ischaemic_heart_disease", sa.Boolean(), nullable=False),
        sa.Column("uncontrolled_heart_failure", sa.Boolean(), nullable=False),
        sa.Column("reduced_lvef", sa.Boolean(), nullable=False),
        sa.Column("conduction_disease", sa.Boolean(), nullable=False),
        sa.Column("brugada_syndrome", sa.Boolean(), nullable=False),
        sa.Column("electrolyte_abnormality", sa.Boolean(), nullable=False),
        sa.Column("bradycardia_symptoms", sa.Boolean(), nullable=False),
        sa.Column("conduction_abnormality", sa.Boolean(), nullable=False),
        sa.Column("pulmonary_symptoms", sa.Boolean(), nullable=False),
        sa.Column("vision_concerns", sa.Boolean(), nullable=False),
        sa.Column("last_ecg_date", sa.Date(), nullable=True),
        sa.Column("last_thyroid_test_date", sa.Date(), nullable=True),
        sa.Column("last_liver_test_date", sa.Date(), nullable=True),
    )

    op.create_table(
        "assessments",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column(
            "patient_id",
            sa.String(length=50),
            sa.ForeignKey("patients.patient_id"),
            nullable=False,
        ),
        sa.Column("medicine", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("alert_count", sa.Integer(), nullable=False),
        sa.Column("alerts", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )

    op.create_index(
        "ix_assessments_patient_id",
        "assessments",
        ["patient_id"],
    )


def downgrade():
    op.drop_index(
        "ix_assessments_patient_id",
        table_name="assessments",
    )
    op.drop_table("assessments")
    op.drop_table("patients")

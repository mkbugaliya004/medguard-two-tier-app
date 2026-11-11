
import os

APP_NAME = "MedGuard API"

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://medguard_user:CHANGE_ME_LOCALLY@db:5432/medguard"
)

DEBUG = os.getenv("DEBUG", "false").lower() == "true"



from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Register models with SQLAlchemy metadata
from app.models import Patient, Assessment

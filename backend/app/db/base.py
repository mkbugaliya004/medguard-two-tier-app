
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


# Import models after defining Base
from app.models.patient import Patient

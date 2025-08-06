from sqlalchemy import Column, Integer, String, Date, JSON
from .database import Base

class WheelSpecification(Base):
    __tablename__ = "wheel_specifications"

    id = Column(Integer, primary_key=True, index=True)
    form_number = Column(String, unique=True, index=True, nullable=False)
    submitted_by = Column(String, index=True, nullable=False)
    submitted_date = Column(Date, nullable=False)
    fields = Column(JSON, nullable=False)
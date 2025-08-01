from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from datetime import datetime

from infrastructure.db.database import Base
from core.type.db_resource import DBResourceType


class PredictDataEntity(Base):
    __tablename__ = DBResourceType.PREDICT_DATA.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    predict1 = Column(Float, nullable=False)
    predict2 = Column(Float, nullable=False)
    predict3 = Column(Float, nullable=False)
    predict4 = Column(Float, nullable=False)
    predict5 = Column(Float, nullable=False)
    predicted_at = Column(DateTime, nullable=False)

    @validates("predicted_at")
    def convert_to_datetime(self, key, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid datetime format for {key}: {value}")
        return value

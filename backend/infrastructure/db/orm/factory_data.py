from sqlalchemy import Column, Integer, Float, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import validates
from datetime import datetime

from core.type.db_resource import DBResourceType
from infrastructure.db.database import Base


class FactoryDataEntity(Base):
    __tablename__ = DBResourceType.FACTORY_DATA.value

    id = Column(Integer, primary_key=True, autoincrement=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    updated_at = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    factory_id = Column(Integer, nullable=False)
    data_id = Column(Integer, nullable=False)
    val1 = Column(Float, nullable=False)
    val2 = Column(Float, nullable=False)
    val3 = Column(Float, nullable=False)
    val4 = Column(Float, nullable=False)
    val5 = Column(Float, nullable=False)
    collected_at = Column(DateTime, nullable=False)

    @validates("collected_at",)
    def convert_to_datetime(self, key, value):
        if isinstance(value, str):
            try:
                return datetime.fromisoformat(value)
            except ValueError:
                raise ValueError(f"Invalid datetime format for {key}: {value}")
        return value

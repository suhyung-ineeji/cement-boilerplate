from datetime import datetime
from pydantic import BaseModel


class FactoryData(BaseModel):
    factory_id: int
    data_id: int
    val1: float
    val2: float
    val3: float
    val4: float
    val5: float
    collected_at: datetime

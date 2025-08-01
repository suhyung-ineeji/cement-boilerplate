from abc import abstractmethod
from pydantic import BaseModel
from datetime import datetime
from typing import ClassVar
from core.type.cache import CacheType


class __BaseCache(BaseModel):
    ttl: int = 7200
    created_at: datetime = datetime.now()

    @abstractmethod
    def get_data_dict(self) -> dict:
        pass

class FactoryDataCache(__BaseCache):
    key: ClassVar[str] = "factory_data" 
    cache_type: CacheType = CacheType.LIST

    factory_id: int
    data_id: int
    val1: float
    val2: float
    val3: float
    val4: float
    val5: float
    collected_at: datetime

    def get_data_dict(self) -> dict:
        return {
            "factory_id": self.factory_id,
            "data_id": self.data_id,
            "val1": self.val1,
            "val2": self.val2,
            "val3": self.val3,
            "val4": self.val4,
            "val5": self.val5,
            "collected_at": self.collected_at.isoformat(),
        }


class PredictDataCache(__BaseCache):
    key: ClassVar[str] = "predict_data"
    cache_type: CacheType = CacheType.STRING

    predict1: float
    predict2: float
    predict3: float
    predict4: float
    predict5: float
    predicted_at: datetime

    def get_data_dict(self) -> dict:
        return {
            "predict1": self.predict1,
            "predict2": self.predict2,
            "predict3": self.predict3,
            "predict4": self.predict4,
            "predict5": self.predict5,
            "predicted_at": self.predicted_at.isoformat(),
        }

from datetime import datetime
from pydantic import BaseModel

class PredictData(BaseModel):
    predict1: float
    predict2: float
    predict3: float
    predict4: float
    predict5: float
    predicted_at: datetime

from datetime import datetime

from core.domain.factory_data import FactoryData
from core.domain.predict_data import PredictData

def predict(data_list: list[FactoryData]) -> PredictData:
    val_list = [0.0 for _ in range(5)]
    for data in data_list:
        val_list[0] += data.val1
        val_list[1] += data.val2
        val_list[2] += data.val3
        val_list[3] += data.val4
        val_list[4] += data.val5
    val_list = [val / len(data_list) for val in val_list]

    return PredictData(
        predict1=val_list[0],
        predict2=val_list[1],
        predict3=val_list[2],
        predict4=val_list[3],
        predict5=val_list[4],
        predicted_at=datetime.now(),
    )
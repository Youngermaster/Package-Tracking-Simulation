from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class MeasurementSchema(BaseModel):
    fecha_hora: datetime = Field(...)
    temperatura: float = Field(..., gt=-273.15)  # Minimum is absolute zero
    latitud: float = Field(..., ge=-90, le=90)
    longitud: float = Field(..., ge=-180, le=180)
    id_sensor: str = Field(...)  # ID of the sensor

    class Config:
        schema_extra = {
            "example": {
                "fecha_hora": "2024-11-06T12:30:00",
                "temperatura": 25.0,
                "latitud": 6.2518,
                "longitud": -75.5636,
                "id_sensor": "sensor_id_example"
            }
        }


class UpdateMeasurementModel(BaseModel):
    fecha_hora: Optional[datetime]
    temperatura: Optional[float]
    latitud: Optional[float]
    longitud: Optional[float]
    id_sensor: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "temperatura": 26.5,
                "latitud": 6.2520,
                "longitud": -75.5637
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}

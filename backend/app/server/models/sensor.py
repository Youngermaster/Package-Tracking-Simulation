from pydantic import BaseModel, Field
from datetime import date


class SensorSchema(BaseModel):
    tipo_sensor: str = Field(..., max_length=10)
    fecha_instalacion: date = Field(...)
    estado: str = Field(..., max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "tipo_sensor": "Temperature",
                "fecha_instalacion": "2023-01-01",
                "estado": "Active"
            }
        }


class UpdateSensorModel(BaseModel):
    tipo_sensor: str = Field(None, max_length=10)
    fecha_instalacion: date = Field(None)
    estado: str = Field(None, max_length=50)

    class Config:
        schema_extra = {
            "example": {
                "tipo_sensor": "Humidity",
                "fecha_instalacion": "2023-01-01",
                "estado": "Inactive"
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

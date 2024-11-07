from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class PackageSchema(BaseModel):
    descripcion: str = Field(..., max_length=255)
    valor: float = Field(..., gt=0)
    ciudad: str = Field(..., max_length=100)
    pais: str = Field(..., max_length=100)
    direccion: str = Field(..., max_length=255)
    fecha_envio: date = Field(...)
    fecha_entrega: Optional[date] = None
    estado_envio: str = Field(..., max_length=50)
    id_sensor: str = Field(...)  # ID of the sensor
    id_cliente: str = Field(...)  # ID of the client (user)

    class Config:
        schema_extra = {
            "example": {
                "descripcion": "Electronics package",
                "valor": 1500.00,
                "ciudad": "Medellín",
                "pais": "Colombia",
                "direccion": "123 Calle Principal",
                "fecha_envio": "2024-11-01",
                "fecha_entrega": "2024-11-10",
                "estado_envio": "In Transit",
                "id_sensor": "sensor_id_example",
                "id_cliente": "client_id_example"
            }
        }


class UpdatePackageModel(BaseModel):
    descripcion: Optional[str]
    valor: Optional[float]
    ciudad: Optional[str]
    pais: Optional[str]
    direccion: Optional[str]
    fecha_envio: Optional[date]
    fecha_entrega: Optional[date]
    estado_envio: Optional[str]
    id_sensor: Optional[str]
    id_cliente: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "estado_envio": "Delivered",
                "fecha_entrega": "2024-11-10"
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

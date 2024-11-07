from pydantic import BaseModel, Field


class VehicleSchema(BaseModel):
    name: str = Field(...)
    emission_gco2_per_km: float = Field(...)
    image_url: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Carro",
                "emission_gco2_per_km": 263,
                "image_url": "http://localhost:8000/static/icons/Car.png",
            }
        }


class UpdateVehicleModel(BaseModel):
    name: str = Field(...)
    emission_gco2_per_km: float = Field(...)
    image_url: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Carro",
                "emission_gco2_per_km": 265,
                "image_url": "https://links.papareact.com/updated",
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

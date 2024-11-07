from pydantic import BaseModel, Field
from typing import Optional, List, Tuple


class RideSchema(BaseModel):
    route_name: str = Field(...)
    distance_traveled: float = Field(...)
    points_obtained: float = Field(...)
    date: str = Field(...)
    user_id: str = Field(...)
    vehicle_used_id: str = Field(...)
    carbon_saved: float = Field(...)
    ride_duration: str = Field(...)
    polyline: List[Tuple[float, float]] = Field(default=[])

    class Config:
        schema_extra = {
            "example": {
                "route_name": "Downtown to Suburb",
                "distance_traveled": 12.5,
                "points_obtained": 25.0,
                "date": "12-10-2023",
                "user_id": "605c72ef1532076878f9ebe5",
                "vehicle_used_id": "605c72ef12234487909ebed2",
                "carbon_saved": 2.5,
                "ride_duration": "00:45:00",
                "polyline": [(6.17511, -75.57432), (6.17550, -75.57398)],
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

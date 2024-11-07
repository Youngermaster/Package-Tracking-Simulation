from pydantic import BaseModel, Field
from typing import Optional


class RedemptionHistorySchema(BaseModel):
    user_id: str = Field(...)
    redeemed_item_id: str = Field(...)
    date_and_time: str = Field(...)
    points_spent: int = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "605c72ef1532076878f9ebe5",
                "redeemed_item_id": "605c72ef12234487909ebed2",
                "date_and_time": "10-10-2023 15:10:00",
                "points_spent": 100
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

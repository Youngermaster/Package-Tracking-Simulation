from pydantic import BaseModel, Field
from typing import Optional


class UserPointsTransactionSchema(BaseModel):
    user_id: str = Field(...)
    transaction_type: str = Field(..., description="Earned or Spent")
    points_amount: int = Field(...)
    date_and_time: str = Field(...)
    transaction_detail: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "user_id": "605c72ef1532076878f9ebe5",
                "transaction_type": "Earned",
                "points_amount": 50,
                "date_and_time": "10-10-2023 15:10:00",
                "transaction_detail": "Ride completion"
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

from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    points: float = Field(default=0.0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@ecodrive.com",
                "password": "securepassword",
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    points: Optional[int]

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane M. Doe",
                "email": "jane.doe@ecodrive.com",
                "password": "newpassword",
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

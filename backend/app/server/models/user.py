from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserSchema(BaseModel):
    name: str = Field(...)
    lastname: str = Field(..., max_length=100)
    email: EmailStr = Field(...)
    phone: str = Field(..., max_length=20)
    address: str = Field(..., max_length=250)
    password: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane",
                "lastname": "Doe",
                "email": "jane.doe@package-tracking.com",
                "phone": "123-456-7890",
                "address": "123 Main St, Anytown, USA",
                "password": "securepassword"
            }
        }


class UpdateUserModel(BaseModel):
    name: Optional[str]
    lastname: Optional[str]
    email: Optional[EmailStr]
    phone: Optional[str]
    address: Optional[str]
    password: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "name": "Jane M.",
                "lastname": "Doe",
                "email": "jane.doe@package-tracking.com",
                "phone": "987-654-3210",
                "address": "456 Elm St, New City, USA",
                "password": "newpassword"
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

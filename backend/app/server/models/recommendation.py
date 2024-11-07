from pydantic import BaseModel, Field


class RecommendationSchema(BaseModel):
    title: str = Field(...)
    description: str = Field(...)
    image_url: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "Duchas Más Cortas",
                "description": "Intenta tomar duchas más cortas. Cuanta menos agua caliente utilices, menos energía se necesitará para calentar el agua.",
                "image_url": "http://localhost:8000/static/images/ducha.png"
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

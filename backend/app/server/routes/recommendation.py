from fastapi import APIRouter, Body, Depends, HTTPException
from server.database.recommendation import (
    add_recommendation,
    delete_recommendation,
    retrieve_recommendation,
    retrieve_recommendations,
    update_recommendation,
)
from server.models.recommendation import RecommendationSchema
from server.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_description="Recommendation data added into the database")
async def add_recommendation_data(recommendation: RecommendationSchema = Body(...), current_user: dict = Depends(get_current_user)):
    recommendation = await add_recommendation(recommendation.dict())
    return {"data": recommendation, "message": "Recommendation added successfully."}


@router.get("/", response_description="Recommendations retrieved")
async def get_recommendations(current_user: dict = Depends(get_current_user)):
    recommendations = await retrieve_recommendations()
    if recommendations:
        return {"data": recommendations, "message": "Recommendations retrieved successfully"}
    return {"data": [], "message": "No recommendations found"}


@router.get("/{id}", response_description="Recommendation data retrieved")
async def get_recommendation_data(id: str, current_user: dict = Depends(get_current_user)):
    recommendation = await retrieve_recommendation(id)
    if recommendation:
        return {"data": recommendation, "message": "Recommendation retrieved successfully"}
    raise HTTPException(status_code=404, detail="Recommendation not found")


@router.put("/{id}", response_description="Recommendation data updated in the database")
async def update_recommendation_data(id: str, recommendation: RecommendationSchema = Body(...), current_user: dict = Depends(get_current_user)):
    recommendation = {k: v for k,
                      v in recommendation.dict().items() if v is not None}
    updated_recommendation = await update_recommendation(id, recommendation)
    if updated_recommendation:
        return {"message": "Recommendation updated successfully"}
    raise HTTPException(status_code=404, detail="Recommendation not found")


@router.delete("/{id}", response_description="Recommendation data deleted from the database")
async def delete_recommendation_data(id: str, current_user: dict = Depends(get_current_user)):
    deleted_recommendation = await delete_recommendation(id)
    if deleted_recommendation:
        return {"message": "Recommendation deleted successfully"}
    raise HTTPException(status_code=404, detail="Recommendation not found")

from bson.objectid import ObjectId
from .config import database

recommendation_collection = database.get_collection(
    "recommendations_collection")


def recommendation_helper(recommendation) -> dict:
    return {
        "id": str(recommendation["_id"]),
        "title": recommendation["title"],
        "description": recommendation["description"],
        "image_url": recommendation["image_url"]
    }


async def retrieve_recommendations():
    recommendations = []
    async for recommendation in recommendation_collection.find():
        recommendations.append(recommendation_helper(recommendation))
    return recommendations


async def add_recommendation(recommendation_data: dict) -> dict:
    recommendation = await recommendation_collection.insert_one(recommendation_data)
    new_recommendation = await recommendation_collection.find_one({"_id": recommendation.inserted_id})
    return recommendation_helper(new_recommendation)


async def retrieve_recommendation(id: str) -> dict:
    recommendation = await recommendation_collection.find_one({"_id": ObjectId(id)})
    if recommendation:
        return recommendation_helper(recommendation)


async def update_recommendation(id: str, data: dict):
    recommendation = await recommendation_collection.find_one({"_id": ObjectId(id)})
    if recommendation:
        updated_recommendation = await recommendation_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        return bool(updated_recommendation.modified_count)


async def delete_recommendation(id: str):
    recommendation = await recommendation_collection.find_one({"_id": ObjectId(id)})
    if recommendation:
        await recommendation_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

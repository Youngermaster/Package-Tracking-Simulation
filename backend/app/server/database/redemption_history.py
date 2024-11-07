from bson.objectid import ObjectId
from .config import database

redemption_history_collection = database.get_collection(
    "redemption_history_collection")


def redemption_history_helper(redemption) -> dict:
    return {
        "id": str(redemption["_id"]),
        "user_id": redemption["user_id"],
        "redeemed_item_id": redemption["redeemed_item_id"],
        "date_and_time": redemption["date_and_time"],
        "points_spent": redemption["points_spent"]
    }

# CRUD operations for Redemption History


async def add_redemption_history(redemption_data: dict) -> dict:
    redemption = await redemption_history_collection.insert_one(redemption_data)
    new_redemption = await redemption_history_collection.find_one({"_id": redemption.inserted_id})
    return redemption_history_helper(new_redemption)


async def retrieve_redemptions(user_id: str = None):
    redemptions = []
    # If user_id is provided, filter the results
    query = {"user_id": user_id} if user_id else {}
    async for redemption in redemption_history_collection.find(query):
        redemptions.append(redemption_history_helper(redemption))
    return redemptions

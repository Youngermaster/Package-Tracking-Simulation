from bson.objectid import ObjectId
from .config import database

ride_collection = database.get_collection("ride_collection")


def ride_helper(ride) -> dict:
    return {
        "id": str(ride["_id"]),
        "route_name": ride["route_name"],
        "distance_traveled": ride["distance_traveled"],
        "points_obtained": ride["points_obtained"],
        "date": ride["date"],
        "user_id": ride["user_id"],
        "vehicle_used_id": ride["vehicle_used_id"],
        "carbon_saved": ride["carbon_saved"],
        "ride_duration": ride["ride_duration"],
        "polyline": ride.get("polyline", []),
    }

# CRUD operations for Rides


async def add_ride(ride_data: dict) -> dict:
    ride = await ride_collection.insert_one(ride_data)
    new_ride = await ride_collection.find_one({"_id": ride.inserted_id})
    return ride_helper(new_ride)


async def retrieve_rides(user_id: str = None):
    rides = []
    query = {"user_id": user_id} if user_id else {}
    async for ride in ride_collection.find(query):
        rides.append(ride_helper(ride))
    return rides

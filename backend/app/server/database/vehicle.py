from bson.objectid import ObjectId
from .config import database

vehicle_collection = database.get_collection("vehicles_collection")


def vehicle_helper(vehicle) -> dict:
    return {
        "id": str(vehicle["_id"]),
        "name": vehicle["name"],
        "emission_gco2_per_km": vehicle["emission_gco2_per_km"],
        "image_url": vehicle["image_url"]
    }


async def retrieve_vehicles():
    vehicles = []
    async for vehicle in vehicle_collection.find():
        vehicles.append(vehicle_helper(vehicle))
    return vehicles


async def add_vehicle(vehicle_data: dict) -> dict:
    vehicle = await vehicle_collection.insert_one(vehicle_data)
    new_vehicle = await vehicle_collection.find_one({"_id": vehicle.inserted_id})
    return vehicle_helper(new_vehicle)


async def retrieve_vehicle(id: str) -> dict:
    vehicle = await vehicle_collection.find_one({"_id": ObjectId(id)})
    if vehicle:
        return vehicle_helper(vehicle)


async def update_vehicle(id: str, data: dict):
    if len(data) < 1:
        return False
    vehicle = await vehicle_collection.find_one({"_id": ObjectId(id)})
    if vehicle:
        updated_vehicle = await vehicle_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_vehicle:
            return True
        return False


async def delete_vehicle(id: str):
    vehicle = await vehicle_collection.find_one({"_id": ObjectId(id)})
    if vehicle:
        await vehicle_collection.delete_one({"_id": ObjectId(id)})
        return True

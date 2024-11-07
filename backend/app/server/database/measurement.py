from bson.objectid import ObjectId
from .config import database

measurement_collection = database.get_collection("measurements_collection")


def measurement_helper(measurement) -> dict:
    return {
        "id": str(measurement["_id"]),
        "fecha_hora": measurement["fecha_hora"],
        "temperatura": measurement["temperatura"],
        "latitud": measurement["latitud"],
        "longitud": measurement["longitud"],
        "id_sensor": measurement["id_sensor"]
    }


async def retrieve_measurements():
    measurements = []
    async for measurement in measurement_collection.find():
        measurements.append(measurement_helper(measurement))
    return measurements


async def add_measurement(measurement_data: dict) -> dict:
    measurement = await measurement_collection.insert_one(measurement_data)
    new_measurement = await measurement_collection.find_one({"_id": measurement.inserted_id})
    return measurement_helper(new_measurement)


async def retrieve_measurement(id: str) -> dict:
    measurement = await measurement_collection.find_one({"_id": ObjectId(id)})
    if measurement:
        return measurement_helper(measurement)


async def update_measurement(id: str, data: dict):
    if len(data) < 1:
        return False
    measurement = await measurement_collection.find_one({"_id": ObjectId(id)})
    if measurement:
        updated_measurement = await measurement_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_measurement.modified_count:
            return True
    return False


async def delete_measurement(id: str):
    measurement = await measurement_collection.find_one({"_id": ObjectId(id)})
    if measurement:
        await measurement_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

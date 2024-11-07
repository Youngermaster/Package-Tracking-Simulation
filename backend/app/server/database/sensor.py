from bson.objectid import ObjectId
from .config import database

sensor_collection = database.get_collection("sensors_collection")


def sensor_helper(sensor) -> dict:
    return {
        "id": str(sensor["_id"]),
        "tipo_sensor": sensor["tipo_sensor"],
        "fecha_instalacion": sensor["fecha_instalacion"],
        "estado": sensor["estado"]
    }


async def retrieve_sensors():
    sensors = []
    async for sensor in sensor_collection.find():
        sensors.append(sensor_helper(sensor))
    return sensors


async def add_sensor(sensor_data: dict) -> dict:
    sensor = await sensor_collection.insert_one(sensor_data)
    new_sensor = await sensor_collection.find_one({"_id": sensor.inserted_id})
    return sensor_helper(new_sensor)


async def retrieve_sensor(id: str) -> dict:
    sensor = await sensor_collection.find_one({"_id": ObjectId(id)})
    if sensor:
        return sensor_helper(sensor)


async def update_sensor(id: str, data: dict):
    if len(data) < 1:
        return False
    sensor = await sensor_collection.find_one({"_id": ObjectId(id)})
    if sensor:
        updated_sensor = await sensor_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_sensor:
            return True
    return False


async def delete_sensor(id: str):
    sensor = await sensor_collection.find_one({"_id": ObjectId(id)})
    if sensor:
        await sensor_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

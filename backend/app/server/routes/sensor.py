from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from server.database.sensor import (
    add_sensor,
    delete_sensor,
    retrieve_sensor,
    retrieve_sensors,
    update_sensor,
)
from server.models.sensor import (
    ErrorResponseModel,
    ResponseModel,
    SensorSchema,
    UpdateSensorModel,
)
from server.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_description="Sensor data added into the database")
async def add_sensor_data(sensor: SensorSchema = Body(...),
                          # current_user: dict = Depends(get_current_user)
                          ):
    sensor = jsonable_encoder(sensor)
    new_sensor = await add_sensor(sensor)
    return ResponseModel(new_sensor, "Sensor added successfully.")


@router.get("/", response_description="Sensors retrieved")
async def get_sensors(
  # current_user: dict = Depends(get_current_user)
  ):
    sensors = await retrieve_sensors()
    if sensors:
        return ResponseModel(sensors, "Sensors data retrieved successfully")
    return ResponseModel(sensors, "Empty list returned")


@router.get("/{id}", response_description="Sensor data retrieved")
async def get_sensor_data(id: str,
                          # current_user: dict = Depends(get_current_user)
                          ):
    sensor = await retrieve_sensor(id)
    if sensor:
        return ResponseModel(sensor, "Sensor data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Sensor doesn't exist.")


@router.put("/{id}", response_description="Sensor data updated in the database")
async def update_sensor_data(id: str, req: UpdateSensorModel = Body(...), 
                            #  current_user: dict = Depends(get_current_user)
                             ):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_sensor = await update_sensor(id, req)
    if updated_sensor:
        return ResponseModel(
            "Sensor with ID: {} update is successful".format(id),
            "Sensor data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the sensor data.",
    )


@router.delete("/{id}", response_description="Sensor data deleted from the database")
async def delete_sensor_data(id: str, 
                            #  current_user: dict = Depends(get_current_user)
                             ):
    deleted_sensor = await delete_sensor(id)
    if deleted_sensor:
        return ResponseModel(
            "Sensor with ID: {} removed".format(id),
            "Sensor deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Sensor with id {0} doesn't exist".format(
            id)
    )

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from server.database.measurement import (
    add_measurement,
    delete_measurement,
    retrieve_measurement,
    retrieve_measurements,
    update_measurement,
)
from server.models.measurement import (
    ErrorResponseModel,
    ResponseModel,
    MeasurementSchema,
    UpdateMeasurementModel,
)
from server.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_description="Measurement data added into the database")
async def add_measurement_data(measurement: MeasurementSchema = Body(...),
                              #  current_user: dict = Depends(get_current_user)
                               ):
    measurement = jsonable_encoder(measurement)
    new_measurement = await add_measurement(measurement)
    return ResponseModel(new_measurement, "Measurement added successfully.")


@router.get("/", response_description="Measurements retrieved")
async def get_measurements(
  # current_user: dict = Depends(get_current_user)
  ):
    measurements = await retrieve_measurements()
    if measurements:
        return ResponseModel(measurements, "Measurements data retrieved successfully")
    return ResponseModel(measurements, "Empty list returned")


@router.get("/{id}", response_description="Measurement data retrieved")
async def get_measurement_data(id: str, 
                              #  current_user: dict = Depends(get_current_user)
                               ):
    measurement = await retrieve_measurement(id)
    if measurement:
        return ResponseModel(measurement, "Measurement data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Measurement doesn't exist.")


@router.put("/{id}", response_description="Measurement data updated in the database")
async def update_measurement_data(id: str, req: UpdateMeasurementModel = Body(...), 
                                  # current_user: dict = Depends(get_current_user)
                                  ):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_measurement = await update_measurement(id, req)
    if updated_measurement:
        return ResponseModel(
            "Measurement with ID: {} update is successful".format(id),
            "Measurement data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the measurement data.",
    )


@router.delete("/{id}", response_description="Measurement data deleted from the database")
async def delete_measurement_data(id: str,
                                  # current_user: dict = Depends(get_current_user)
                                  ):
    deleted_measurement = await delete_measurement(id)
    if deleted_measurement:
        return ResponseModel(
            "Measurement with ID: {} removed".format(id),
            "Measurement deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Measurement with id {0} doesn't exist".format(id)
    )

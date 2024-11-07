from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from server.database.vehicle import (
    add_vehicle,
    delete_vehicle,
    retrieve_vehicle,
    retrieve_vehicles,
    update_vehicle,
)

from server.models.vehicle import (
    ErrorResponseModel,
    ResponseModel,
    VehicleSchema,
    UpdateVehicleModel,
)
from server.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_description="Vehicle data added into the database")
async def add_vehicle_data(vehicle: VehicleSchema = Body(...), current_user: dict = Depends(get_current_user)):
    vehicle = jsonable_encoder(vehicle)
    new_vehicle = await add_vehicle(vehicle)
    return ResponseModel(new_vehicle, "Vehicle added successfully.")


@router.get("/", response_description="Vehicles retrieved")
async def get_vehicles(current_user: dict = Depends(get_current_user)):
    # You can access the current_user if needed, or just keep it in Depends() for protection
    vehicles = await retrieve_vehicles()
    if vehicles:
        return ResponseModel(vehicles, "Vehicles data retrieved successfully")
    return ResponseModel(vehicles, "Empty list returned")


@router.get("/{id}", response_description="Vehicle data retrieved")
async def get_vehicle_data(id: str, current_user: dict = Depends(get_current_user)):
    vehicle = await retrieve_vehicle(id)
    if vehicle:
        return ResponseModel(vehicle, "Vehicle data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Vehicle doesn't exist.")


@router.put("/{id}", response_description="Vehicle data updated in the database")
async def update_vehicle_data(id: str, req: UpdateVehicleModel = Body(...), current_user: dict = Depends(get_current_user)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_vehicle = await update_vehicle(id, req)
    if updated_vehicle:
        return ResponseModel(
            "Vehicle with ID: {} update is successful".format(id),
            "Vehicle data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the vehicle data.",
    )


@router.delete("/{id}", response_description="Vehicle data deleted from the database")
async def delete_vehicle_data(id: str, current_user: dict = Depends(get_current_user)):
    deleted_vehicle = await delete_vehicle(id)
    if deleted_vehicle:
        return ResponseModel(
            "Vehicle with ID: {} removed".format(id),
            "Vehicle deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Vehicle with id {0} doesn't exist".format(
            id)
    )

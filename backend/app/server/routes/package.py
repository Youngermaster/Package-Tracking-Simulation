from fastapi import APIRouter, Body, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from server.database.package import (
    add_package,
    delete_package,
    retrieve_package,
    retrieve_packages,
    update_package,
    retrieve_packages_by_sensor_id,
    retrieve_packages_by_sensor_type
)
from server.models.package import (
    ErrorResponseModel,
    ResponseModel,
    PackageSchema,
    UpdatePackageModel,
)
from server.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_description="Package data added into the database")
async def add_package_data(package: PackageSchema = Body(...), 
                          #  current_user: dict = Depends(get_current_user)
                           ):
    package = jsonable_encoder(package)
    new_package = await add_package(package)
    return ResponseModel(new_package, "Package added successfully.")


@router.get("/", response_description="Packages retrieved")
async def get_packages(
  # current_user: dict = Depends(get_current_user)
  ):
    packages = await retrieve_packages()
    if packages:
        return ResponseModel(packages, "Packages data retrieved successfully")
    return ResponseModel(packages, "Empty list returned")


@router.get("/{id}", response_description="Package data retrieved")
async def get_package_data(id: str,
                          #  current_user: dict = Depends(get_current_user)
                           ):
    package = await retrieve_package(id)
    if package:
        return ResponseModel(package, "Package data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "Package doesn't exist.")


@router.put("/{id}", response_description="Package data updated in the database")
async def update_package_data(id: str, req: UpdatePackageModel = Body(...),
                              # current_user: dict = Depends(get_current_user)
                              ):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_package = await update_package(id, req)
    if updated_package:
        return ResponseModel(
            "Package with ID: {} update is successful".format(id),
            "Package data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the package data.",
    )


@router.delete("/{id}", response_description="Package data deleted from the database")
async def delete_package_data(id: str,
                              # current_user: dict = Depends(get_current_user)
                              ):
    deleted_package = await delete_package(id)
    if deleted_package:
        return ResponseModel(
            "Package with ID: {} removed".format(id),
            "Package deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "Package with id {0} doesn't exist".format(id)
    )


@router.get("/sensor/type", response_description="Retrieve packages by sensor type")
async def get_packages_by_sensor_type(sensor_type: str = Query(..., description="Type of sensor to filter packages by"),
                                      # current_user: dict = Depends(get_current_user)
                                      ):
    packages = await retrieve_packages_by_sensor_type(sensor_type)
    if packages:
        return ResponseModel(packages, "Packages data retrieved successfully")
    return ResponseModel([], "No packages found for this sensor type")


@router.get("/sensor/{sensor_id}", response_description="Retrieve packages by sensor ID")
async def get_packages_by_sensor_id(sensor_id: str,
                                    # current_user: dict = Depends(get_current_user)
                                    ):
    packages = await retrieve_packages_by_sensor_id(sensor_id)
    if packages:
        return ResponseModel(packages, "Packages data retrieved successfully")
    return ResponseModel([], "No packages found for this sensor ID")


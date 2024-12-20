from fastapi.security import OAuth2PasswordRequestForm
from server.utils import create_access_token
from passlib.context import CryptContext
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from server.database.user import (
    add_user,
    delete_user,
    retrieve_user,
    retrieve_user_by_email,
    retrieve_users,
    update_user,
    retrieve_packages_by_user_id,
    retrieve_packages_by_user_email
)

from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
    UpdateUserModel,
)
from server.dependencies import get_current_user
from server.routes.authentication import get_password_hash

router = APIRouter()


@router.get("/me", response_description="Get current user details")
async def get_current_user_details(current_user: dict = Depends(get_current_user)):
    return ResponseModel(current_user, "User data retrieved successfully")


@router.put("/me", response_description="Update current user details")
async def update_current_user_details(req: UpdateUserModel = Body(...), current_user: dict = Depends(get_current_user)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    
    # Check if 'password' is in the request and hash it before updating
    if "password" in req:
        req["password"] = get_password_hash(req["password"])
    
    updated_user = await update_user(current_user["_id"], req)
    if updated_user:
        return ResponseModel("Update successful", "User data updated successfully")
    return ErrorResponseModel("An error occurred", 404, "There was an error updating the user data.")


@router.delete("/me", response_description="Delete current user")
async def delete_current_user_data(current_user: dict = Depends(get_current_user)):
    deleted_user = await delete_user(current_user["_id"])
    if deleted_user:
        return ResponseModel("User removed", "User deleted successfully")
    return ErrorResponseModel("An error occurred", 404, "There was an error deleting the user.")



@router.get("/{user_id}/packages", response_description="Retrieve packages by user ID")
async def get_packages_by_user_id(user_id: str):
    packages = await retrieve_packages_by_user_id(user_id)
    if packages:
        return ResponseModel(packages, "Packages data retrieved successfully")
    return ResponseModel([], "No packages found for this user ID")


@router.get("/email/{user_email}/packages", response_description="Retrieve packages by user email")
async def get_packages_by_user_email(user_email: str):
    packages = await retrieve_packages_by_user_email(user_email)
    if packages:
        return ResponseModel(packages, "Packages data retrieved successfully")
    return ResponseModel([], "No packages found for this user email")


@router.post("/", response_description="User data added into the database")
async def add_user_data(user: UserSchema = Body(...),
                        # current_user: dict = Depends(get_current_user)
                        ):
    user = jsonable_encoder(user)
    new_user = await add_user(user)
    return ResponseModel(new_user, "User added successfully.")


@router.get("/", response_description="Users retrieved")
async def get_users(
    # current_user: dict = Depends(get_current_user)
    ):
    # You can access the current_user if needed, or just keep it in Depends() for protection
    users = await retrieve_users()
    if users:
        return ResponseModel(users, "Users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="User data retrieved")
async def get_user_data(id: str, 
                        # current_user: dict = Depends(get_current_user)
                        ):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.put("/{id}", response_description="User data updated in the database")
async def update_user_data(id: str, req: UpdateUserModel = Body(...),
                        #    current_user: dict = Depends(get_current_user)
                           ):
    req = {k: v for k, v in req.dict().items() if v is not None}
    
    # Check if 'password' is in the request and hash it before updating
    if "password" in req:
        req["password"] = get_password_hash(req["password"])
    
    updated_user = await update_user(id, req)
    if updated_user:
        return ResponseModel(
            "User with ID: {} update is successful".format(id),
            "User data updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the user data.",
    )


@router.get("/email/{email}", response_description="User data retrieved by email")
async def get_user_by_email(email: str, 
                            # current_user: dict = Depends(get_current_user)
                            ):
    user = await retrieve_user_by_email(email)
    if user:
        return ResponseModel(user, "User data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "User doesn't exist.")


@router.delete("/{id}", response_description="User data deleted from the database")
async def delete_user_data(id: str, 
                        #    current_user: dict = Depends(get_current_user)
                           ):
    deleted_user = await delete_user(id)
    if deleted_user:
        return ResponseModel(
            "User with ID: {} removed".format(id),
            "User deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "User with id {0} doesn't exist".format(id)
    )

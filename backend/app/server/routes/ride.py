from fastapi import APIRouter, Body, Depends, HTTPException
from server.database.ride import (
    add_ride,
    retrieve_rides,
)
from server.models.ride import RideSchema, ResponseModel, ErrorResponseModel
from server.dependencies import get_current_user
from server.database.user import update_user, retrieve_user
from server.database.user_points_transaction import add_user_points_transaction
import datetime

router = APIRouter()


@router.post("/", response_description="Ride data added into the database")
async def add_ride_data(ride: RideSchema = Body(...),
                        #current_user: dict = Depends(get_current_user)
                        ):
    ride_data = ride.dict()

    # Step 1: Increment User Points
    user_id = ride.user_id
    user = await retrieve_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User doesn't exist.")

    updated_points = user["points"] + ride.points_obtained
    updated_user = await update_user(user_id, {"points": updated_points})
    if not updated_user:
        raise HTTPException(
            status_code=404, detail="There was an error updating the user points.")

    # Step 2: Add the ride data
    added_ride = await add_ride(ride_data)

    # Step 3: Log Transaction (points earned)
    transaction_data = {
        "user_id": user_id,
        "transaction_type": "Earned",
        "points_amount": ride.points_obtained,
        "date_and_time": str(datetime.datetime.now()),
        "transaction_detail": f"Obtenidos {ride.points_obtained} puntos obtenido del viaje {added_ride['id']}."
    }
    added_transaction = await add_user_points_transaction(transaction_data)

    return ResponseModel(added_ride, "Ride added, user points updated, and transaction logged successfully.")


@router.get("/", response_description="Rides retrieved")
async def get_rides(user_id: str = None, 
                    #current_user: dict = Depends(get_current_user)
                    ):
    rides = await retrieve_rides(user_id)
    if rides:
        return ResponseModel(rides, "Rides data retrieved successfully.")
    return ResponseModel(rides, "No rides found.")

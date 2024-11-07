from fastapi import APIRouter, Body, Depends, HTTPException
from server.database.redemption_history import (
    add_redemption_history,
    retrieve_redemptions,
)
from server.database.user_points_transaction import add_user_points_transaction
from server.database.user import update_user, retrieve_user
from server.models.redemption_history import RedemptionHistorySchema, ResponseModel, ErrorResponseModel
from server.dependencies import get_current_user
import datetime

router = APIRouter()


@router.post("/", response_description="Redemption data added into the database")
async def add_redemption_data(redemption: RedemptionHistorySchema = Body(...), current_user: dict = Depends(get_current_user)):
    # Step 1: Decrement User Points
    user_id = redemption.user_id
    user = await retrieve_user(user_id)
    if not user:
        return ErrorResponseModel("An error occurred", 404, "User doesn't exist.")
    if user["points"] < redemption.points_spent:
        return ErrorResponseModel("An error occurred", 400, "Not enough points.")

    updated_user = await update_user(user_id, {"points": user["points"] - redemption.points_spent})
    if not updated_user:
        return ErrorResponseModel("An error occurred", 404, "There was an error updating the user points.")

    # Step 2: Log Redemption
    redemption_data = redemption.dict()
    redemption_data["user_id"] = user_id
    added_redemption = await add_redemption_history(redemption_data)

    # Step 3: Log Transaction (points spent)
    transaction_data = {
        "user_id": user_id,
        "transaction_type": "spent",
        "points_amount": redemption.points_spent,
        # Use a proper datetime format
        "date_and_time": str(datetime.datetime.now()),
        "transaction_detail": f"Redeemed {redemption.points_spent} points for item {redemption.redeemed_item_id}."
    }
    added_transaction = await add_user_points_transaction(transaction_data)

    return ResponseModel(added_redemption, "Redemption added and transaction logged successfully.")


@router.get("/", response_description="Redemptions retrieved")
async def get_redemptions(user_id: str = None, current_user: dict = Depends(get_current_user)):
    redemptions = await retrieve_redemptions(user_id)
    if redemptions:
        return ResponseModel(redemptions, "Redemptions data retrieved successfully.")
    return ResponseModel(redemptions, "No redemptions found.")

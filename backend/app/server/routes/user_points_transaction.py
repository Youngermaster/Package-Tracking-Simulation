from fastapi import APIRouter, Body, Depends, HTTPException
from server.database.user_points_transaction import (
    add_user_points_transaction,
    retrieve_transactions,
)
from server.models.user_points_transaction import UserPointsTransactionSchema, ResponseModel, ErrorResponseModel
from server.dependencies import get_current_user

router = APIRouter()


@router.post("/", response_description="User points transaction data added into the database")
async def add_transaction_data(transaction: UserPointsTransactionSchema = Body(...), current_user: dict = Depends(get_current_user)):
    transaction = await add_user_points_transaction(transaction.dict())
    return ResponseModel(transaction, "Transaction added successfully.")


@router.get("/", response_description="User points transactions retrieved")
async def get_transactions(user_id: str = None, current_user: dict = Depends(get_current_user)):
    transactions = await retrieve_transactions(user_id)
    if transactions:
        return ResponseModel(transactions, "Transactions data retrieved successfully.")
    return ResponseModel(transactions, "No transactions found.")

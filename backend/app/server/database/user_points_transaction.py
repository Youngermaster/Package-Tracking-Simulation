from .config import database

user_points_transaction_collection = database.get_collection(
    "user_points_transaction_collection"
)


def user_points_transaction_helper(transaction) -> dict:
    return {
        "id": str(transaction["_id"]),
        "user_id": transaction["user_id"],
        "transaction_type": transaction["transaction_type"],
        "points_amount": transaction["points_amount"],
        "date_and_time": transaction["date_and_time"],
        "transaction_detail": transaction["transaction_detail"]
    }

# CRUD operations for User Points Transaction


async def add_user_points_transaction(transaction_data: dict) -> dict:
    transaction = await user_points_transaction_collection.insert_one(transaction_data)
    new_transaction = await user_points_transaction_collection.find_one({"_id": transaction.inserted_id})
    return user_points_transaction_helper(new_transaction)


async def retrieve_transactions(user_id: str = None):
    transactions = []
    query = {"user_id": user_id} if user_id else {}
    async for transaction in user_points_transaction_collection.find(query):
        transactions.append(user_points_transaction_helper(transaction))
    return transactions

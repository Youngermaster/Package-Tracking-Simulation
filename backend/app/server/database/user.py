from bson.objectid import ObjectId
from .config import database
from .package import package_collection, package_helper

user_collection = database.get_collection("users_collection")


def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "lastname": user["lastname"],
        "email": user["email"],
        "phone": user["phone"],
        "address": user["address"],
        "password": user.get("password", ""),
    }


async def retrieve_users():
    users = []
    async for user in user_collection.find():
        users.append(user_helper(user))
    return users


async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


async def add_user(user_data: dict) -> dict:
    user = await user_collection.insert_one(user_data)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


async def update_user(id: str, data: dict):
    if len(data) < 1:
        return False
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = await user_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


async def retrieve_user_by_email(email: str) -> dict:
    user = await user_collection.find_one({"email": email})
    if user:
        return user_helper(user)


async def delete_user(id: str):
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        await user_collection.delete_one({"_id": ObjectId(id)})
        return True


async def update_user_points(user_id: str, points: float):
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    if not user:
        return None

    updated_points = user["points"] + points
    updated_user = await user_collection.update_one(
        {"_id": ObjectId(user_id)}, {"$set": {"points": updated_points}}
    )
    if updated_user.modified_count:
        return True
    return False


async def retrieve_packages_by_user_id(user_id: str):
    """Retrieve all packages associated with a specific user ID."""
    packages = []
    async for package in package_collection.find({"id_cliente": user_id}):
        packages.append(package_helper(package))
    return packages


async def retrieve_packages_by_user_email(user_email: str):
    """Obtener todos los paquetes asociados a un correo electrónico específico del usuario usando agregación."""
    packages = []
    async for package in package_collection.aggregate([
        {
            # Realiza un lookup para unir los documentos de paquetes con la colección de usuarios (users_collection)
            # utilizando id_cliente en paquetes y _id en usuarios como campos de unión.
            "$lookup": {
                "from": "users_collection",  # La colección con la que se unirá
                # Define una variable clientId que toma el valor de id_cliente en paquetes
                "let": {"clientId": "$id_cliente"},
                # Define una pipeline para filtrar los usuarios basados en la conversión de ObjectId y el email del usuario
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$and": [
                                # Compara _id en la colección de usuarios con clientId (convertido a ObjectId)
                                {"$eq": ["$_id", {"$toObjectId": "$$clientId"}]},
                                # Compara el email en usuarios con el user_email proporcionado
                                {"$eq": ["$email", user_email]}
                            ]
                        }
                    }}
                ],
                "as": "user_info"  # Nombra los datos unidos como user_info en el documento de salida
            }
        },
        {
            # Descompone el array user_info para convertirlo en un objeto único
            "$unwind": "$user_info"
        },
        {
            # Opcionalmente excluye el campo user_info del resultado final para simplificar la salida
            "$project": {
                "user_info": 0  # Establece en 0 para excluir user_info de la salida
            }
        }
    ]):
        # Añade cada paquete que coincida, formateado por la función package_helper, a la lista de resultados
        packages.append(package_helper(package))
    
    return packages

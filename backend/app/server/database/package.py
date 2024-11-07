from bson.objectid import ObjectId
from .config import database

package_collection = database.get_collection("packages_collection")


def package_helper(package) -> dict:
    return {
        "id": str(package["_id"]),
        "descripcion": package["descripcion"],
        "valor": package["valor"],
        "ciudad": package["ciudad"],
        "pais": package["pais"],
        "direccion": package["direccion"],
        "fecha_envio": package["fecha_envio"],
        "fecha_entrega": package.get("fecha_entrega"),
        "estado_envio": package["estado_envio"],
        "id_sensor": package["id_sensor"],
        "id_cliente": package["id_cliente"]
    }


async def retrieve_packages():
    packages = []
    async for package in package_collection.find():
        packages.append(package_helper(package))
    return packages


async def add_package(package_data: dict) -> dict:
    package = await package_collection.insert_one(package_data)
    new_package = await package_collection.find_one({"_id": package.inserted_id})
    return package_helper(new_package)


async def retrieve_package(id: str) -> dict:
    package = await package_collection.find_one({"_id": ObjectId(id)})
    if package:
        return package_helper(package)


async def update_package(id: str, data: dict):
    if len(data) < 1:
        return False
    package = await package_collection.find_one({"_id": ObjectId(id)})
    if package:
        updated_package = await package_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_package.modified_count:
            return True
    return False


async def delete_package(id: str):
    package = await package_collection.find_one({"_id": ObjectId(id)})
    if package:
        await package_collection.delete_one({"_id": ObjectId(id)})
        return True
    return False

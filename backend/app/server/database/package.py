from bson.objectid import ObjectId
from .config import database
from .sensor import sensor_collection

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


async def retrieve_packages_by_sensor_id(sensor_id: str):
    """Retrieve all packages associated with a specific sensor ID"""
    packages = []
    async for package in package_collection.find({"id_sensor": sensor_id}):
        packages.append(package_helper(package))
    return packages

async def retrieve_packages_by_sensor_type(sensor_type: str):
    """Obtener todos los paquetes asociados con un tipo específico de sensor usando agregación y conversión de ObjectId."""
    packages = []
    async for package in package_collection.aggregate([
        {
            # Realiza un lookup para unir los documentos de paquetes con la colección de sensores (sensors_collection) 
            # utilizando id_sensor y _id como campos de unión
            "$lookup": {
                "from": "sensors_collection",  # La colección con la que se unirá
                # Define una variable sensorId que convierte el id_sensor de cadena a ObjectId
                "let": {"sensorId": {"$toObjectId": "$id_sensor"}},
                # Define una pipeline para filtrar los sensores basados en el ObjectId convertido y el tipo_sensor
                "pipeline": [
                    {"$match": {
                        "$expr": {
                            "$and": [
                                {"$eq": ["$_id", "$$sensorId"]},  # Compara _id en sensores con la variable sensorId
                                {"$eq": ["$tipo_sensor", sensor_type]}  # Compara tipo_sensor con el valor proporcionado
                            ]
                        }
                    }}
                ],
                "as": "sensor_info"  # Nombra los datos unidos como sensor_info en el documento de salida
            }
        },
        {
            # Descompone el array sensor_info para convertirlo en un objeto único
            "$unwind": "$sensor_info"
        },
        {
            # Opcionalmente excluye el campo sensor_info del resultado final para simplificar la salida
            "$project": {
                "sensor_info": 0  # Establece en 0 para excluir sensor_info de la salida
            }
        }
    ]):
        # Añade cada paquete que coincida, formateado por la función package_helper, a la lista de resultados
        packages.append(package_helper(package))
    
    return packages

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from server.routes.authentication import router as AuthRouter
from server.routes.user import router as UserRouter
from server.routes.sensor import router as SensorRouter
from server.routes.package import router as PackageRouter
from decouple import config


is_production = config('PROJECT_ENVIRONMENT', default="DEVELOPMENT")

if is_production == 'RELEASE':
    app = FastAPI(
        docs_url=None,  # Disable docs (Swagger UI)
        redoc_url=None,  # Disable redoc
    )
else:
    app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter, tags=["Authentication"])
app.include_router(UserRouter, tags=["User"], prefix="/user")
app.include_router(SensorRouter, tags=["Sensor"], prefix="/sensor")
app.include_router(PackageRouter, tags=["Package"], prefix="/package")


@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido al monitoreo de paquetes!"}

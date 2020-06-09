from fastapi import APIRouter

from backend.app.api.api_v1.endpoints import settings, sensors, participants

api_router = APIRouter()
api_router.include_router(participants.router, prefix="/participants", tags=["participants"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])

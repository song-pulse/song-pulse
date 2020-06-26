from fastapi import APIRouter

from app.api.api_v1.endpoints import participants, sensors, settings, spotify

api_router = APIRouter()
api_router.include_router(participants.router, prefix="/participants", tags=["participants"])
api_router.include_router(sensors.router, prefix="/sensors", tags=["sensors"])
api_router.include_router(settings.router, prefix="/settings", tags=["settings"])
api_router.include_router(spotify.router, prefix="/spotify", tags=["spotify"])

from fastapi import APIRouter
from api.v1.auth.router import router as auth_router
from api.v1.emergencies.router import router as emergencies_router
from api.v1.hospitals.router import router as hospitals_router
from api.v1.resources.router import router as resources_router
from api.v1.websockets.router import router as websocket_router
from api.v1.health.router import router as health_router

from api.v1.safety.router import router as safety_router
from api.v1.volunteers.router import router as volunteers_router
from api.v1.business.router import router as business_router
from api.v1.moderation.router import router as moderation_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(emergencies_router)
api_router.include_router(hospitals_router)
api_router.include_router(resources_router)
api_router.include_router(websocket_router)
api_router.include_router(safety_router)
api_router.include_router(volunteers_router)
api_router.include_router(business_router)
api_router.include_router(moderation_router)

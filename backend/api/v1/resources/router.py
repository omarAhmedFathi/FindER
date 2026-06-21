from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from core.database import get_db
from api.v1.auth.dependencies import require_role
from api.v1.auth.models import UserRole

router = APIRouter(prefix="/resources", tags=["resources"])

@router.get("/")
@cache(expire=300) # 5 minutes TTL
async def list_resources(
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role([UserRole.EMERGENCY_MANAGER]))
):
    # Simulated heavy query
    return {"ambulances": [], "fire_trucks": []}

@router.post("/dispatch")
async def dispatch_resource(
    resource_id: str, emergency_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role([UserRole.EMERGENCY_MANAGER]))
):
    # Dispatch invalidates cache or depends on real-time WS
    return {"status": "Dispatched", "eta_minutes": 5}

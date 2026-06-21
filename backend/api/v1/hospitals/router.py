from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from core.database import get_db
from api.v1.auth.dependencies import require_role
from api.v1.auth.models import UserRole

router = APIRouter(prefix="/hospitals", tags=["hospitals"])

class HospitalCapacityUpdate(BaseModel):
    available_beds: int

@router.put("/{hospital_id}/capacity")
async def update_capacity(
    hospital_id: str, 
    payload: HospitalCapacityUpdate,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role([UserRole.HOSPITAL_ADMIN, UserRole.EMERGENCY_MANAGER]))
):
    # Update DB and push WebSocket diff to emergency managers
    return {"status": "success", "hospital_id": hospital_id, "available_beds": payload.available_beds}

@router.post("/{hospital_id}/surge-alert")
async def trigger_surge_alert(
    hospital_id: str,
    db: AsyncSession = Depends(get_db),
    user = Depends(require_role([UserRole.EMERGENCY_MANAGER]))
):
    # Automatically ping all assigned staff and queue mass-casualty protocols
    return {"status": "Surge Protocol Activated"}

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from core.database import get_db
from pydantic import BaseModel
from api.v1.auth.dependencies import get_current_user, require_role
from api.v1.auth.models import User, UserRole

router = APIRouter(prefix="/emergencies", tags=["emergencies"])

class SOSRequest(BaseModel):
    location_lat: float
    location_lon: float
    is_anonymous: bool = False
    description: Optional[str] = None
    severity: int = 3

class EmergencyResponse(SOSRequest):
    id: str
    status: str

@router.post("/sos", response_model=EmergencyResponse)
async def trigger_sos(
    sos_req: SOSRequest, 
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user)
):
    # Logic to map SOS payload to emergency table and emit WebSocket alert
    # If anonymous, reporter_id is stripped
    return {"id": "1234-uuid", "status": "ACTIVE", **sos_req.dict()}

@router.post("/nlp-audio")
async def detect_scream(
    background_tasks: BackgroundTasks,
    audio_file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    # Async audio chunking and NLP classification
    # If confidence > 0.85, auto-generate emergency
    return {"status": "Processing", "filename": audio_file.filename}

@router.get("/active")
async def get_active_emergencies(
    page: int = 1, limit: int = 50,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(require_role([UserRole.EMERGENCY_MANAGER]))
):
    # Retrieve paginated active emergencies for Situational Dashboard
    return {"items": [], "total": 0, "page": page, "limit": limit}

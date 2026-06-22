from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from typing import List, Optional
from core.database import get_db
from api.v1.auth.dependencies import get_current_user
from api.v1.auth.models import User
from api.v1.emergencies.models import Emergency, EmergencyStatus
from api.v1.emergencies.schemas import EmergencyCreate, EmergencyUpdate, EmergencyResponse

router = APIRouter(prefix="/emergencies", tags=["emergencies"])


@router.post("/", response_model=EmergencyResponse, status_code=status.HTTP_201_CREATED)
async def create_emergency(
    payload: EmergencyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    reporter_id = None if payload.is_anonymous else (current_user.id if current_user else None)
    emergency = Emergency(
        reporter_id=reporter_id,
        location_lat=payload.location_lat,
        location_lon=payload.location_lon,
        description=payload.description,
        severity=payload.severity,
        status=EmergencyStatus.ACTIVE,
    )
    db.add(emergency)
    await db.commit()
    await db.refresh(emergency)
    return emergency


@router.post("/sos", response_model=EmergencyResponse, status_code=status.HTTP_201_CREATED)
async def trigger_sos(
    payload: EmergencyCreate,
    db: AsyncSession = Depends(get_db),
    current_user: Optional[User] = Depends(get_current_user),
):
    reporter_id = None if payload.is_anonymous else (current_user.id if current_user else None)
    emergency = Emergency(
        reporter_id=reporter_id,
        location_lat=payload.location_lat,
        location_lon=payload.location_lon,
        description=payload.description or "SOS Alert",
        severity=5,
        status=EmergencyStatus.ACTIVE,
    )
    db.add(emergency)
    await db.commit()
    await db.refresh(emergency)
    return emergency


@router.get("/active", response_model=List[EmergencyResponse])
async def get_active_emergencies(
    page: int = 1,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        select(Emergency)
        .where(Emergency.status == EmergencyStatus.ACTIVE)
        .order_by(desc(Emergency.created_at))
        .offset((page - 1) * limit)
        .limit(limit)
    )
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/", response_model=List[EmergencyResponse])
async def list_emergencies(
    page: int = 1,
    limit: int = 50,
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Emergency).order_by(desc(Emergency.created_at))
    if status_filter:
        try:
            s = EmergencyStatus(status_filter.upper())
            query = query.where(Emergency.status == s)
        except ValueError:
            pass
    query = query.offset((page - 1) * limit).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{emergency_id}", response_model=EmergencyResponse)
async def get_emergency(
    emergency_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Emergency).where(Emergency.id == emergency_id))
    emergency = result.scalars().first()
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    return emergency


@router.patch("/{emergency_id}", response_model=EmergencyResponse)
async def update_emergency(
    emergency_id: str,
    payload: EmergencyUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Emergency).where(Emergency.id == emergency_id))
    emergency = result.scalars().first()
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    if payload.status is not None:
        emergency.status = payload.status
    if payload.description is not None:
        emergency.description = payload.description
    if payload.severity is not None:
        emergency.severity = payload.severity
    await db.commit()
    await db.refresh(emergency)
    return emergency


@router.post("/nlp-audio")
async def detect_scream(audio_file: UploadFile = File(...)):
    return {"status": "Processing", "filename": audio_file.filename, "confidence": 0.0}

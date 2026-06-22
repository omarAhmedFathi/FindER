from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import List, Optional
from core.database import get_db
from api.v1.auth.dependencies import get_current_user, require_role
from api.v1.auth.models import User, UserRole
from api.v1.hospitals.models import Hospital
from api.v1.hospitals.schemas import HospitalCreate, HospitalUpdate, HospitalResponse
import math

router = APIRouter(prefix="/hospitals", tags=["hospitals"])


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    return R * 2 * math.asin(math.sqrt(a))


@router.get("/", response_model=List[HospitalResponse])
async def list_hospitals(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Hospital).order_by(Hospital.name))
    return result.scalars().all()


@router.post("/", response_model=HospitalResponse, status_code=status.HTTP_201_CREATED)
async def create_hospital(
    payload: HospitalCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EMERGENCY_MANAGER])),
):
    hospital = Hospital(
        name=payload.name,
        location_lat=payload.location_lat,
        location_lon=payload.location_lon,
        total_beds=payload.total_beds,
        available_beds=payload.available_beds,
        trauma_level=payload.trauma_level,
        admin_id=current_user.id,
    )
    db.add(hospital)
    await db.commit()
    await db.refresh(hospital)
    return hospital


@router.get("/nearest", response_model=List[HospitalResponse])
async def nearest_hospitals(
    lat: float,
    lon: float,
    limit: int = 5,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Hospital))
    hospitals = result.scalars().all()
    with_dist = sorted(hospitals, key=lambda h: haversine(lat, lon, float(h.location_lat), float(h.location_lon)))
    return with_dist[:limit]


@router.get("/{hospital_id}", response_model=HospitalResponse)
async def get_hospital(
    hospital_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return hospital


@router.put("/{hospital_id}/capacity", response_model=HospitalResponse)
async def update_capacity(
    hospital_id: str,
    payload: HospitalUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.HOSPITAL_ADMIN, UserRole.EMERGENCY_MANAGER])),
):
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    if payload.available_beds is not None:
        hospital.available_beds = payload.available_beds
    if payload.total_beds is not None:
        hospital.total_beds = payload.total_beds
    if payload.trauma_level is not None:
        hospital.trauma_level = payload.trauma_level
    await db.commit()
    await db.refresh(hospital)
    return hospital


@router.post("/{hospital_id}/surge-alert")
async def trigger_surge_alert(
    hospital_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EMERGENCY_MANAGER])),
):
    result = await db.execute(select(Hospital).where(Hospital.id == hospital_id))
    hospital = result.scalars().first()
    if not hospital:
        raise HTTPException(status_code=404, detail="Hospital not found")
    return {"status": "Surge Protocol Activated", "hospital": hospital.name}

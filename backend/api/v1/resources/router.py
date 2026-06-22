from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Optional
from core.database import get_db
from api.v1.auth.dependencies import get_current_user, require_role
from api.v1.auth.models import User, UserRole
from api.v1.resources.models import Resource, ResourceType
from api.v1.resources.schemas import ResourceCreate, ResourceUpdate, ResourceResponse

router = APIRouter(prefix="/resources", tags=["resources"])


@router.get("/", response_model=List[ResourceResponse])
async def list_resources(
    resource_type: Optional[str] = None,
    status_filter: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = select(Resource)
    if resource_type:
        try:
            rt = ResourceType(resource_type.upper())
            query = query.where(Resource.type == rt)
        except ValueError:
            pass
    if status_filter:
        query = query.where(Resource.status == status_filter.upper())
    result = await db.execute(query)
    return result.scalars().all()


@router.post("/", response_model=ResourceResponse, status_code=status.HTTP_201_CREATED)
async def create_resource(
    payload: ResourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EMERGENCY_MANAGER])),
):
    resource = Resource(
        name=payload.name,
        type=payload.type,
        location_lat=payload.location_lat,
        location_lon=payload.location_lon,
        status=payload.status,
    )
    db.add(resource)
    await db.commit()
    await db.refresh(resource)
    return resource


@router.get("/{resource_id}", response_model=ResourceResponse)
async def get_resource(
    resource_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalars().first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    return resource


@router.patch("/{resource_id}", response_model=ResourceResponse)
async def update_resource(
    resource_id: str,
    payload: ResourceUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EMERGENCY_MANAGER])),
):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalars().first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    if payload.status is not None:
        resource.status = payload.status
    if payload.assigned_to is not None:
        resource.assigned_to = payload.assigned_to
    if payload.location_lat is not None:
        resource.location_lat = payload.location_lat
    if payload.location_lon is not None:
        resource.location_lon = payload.location_lon
    await db.commit()
    await db.refresh(resource)
    return resource


@router.post("/dispatch")
async def dispatch_resource(
    resource_id: str,
    emergency_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_role([UserRole.EMERGENCY_MANAGER])),
):
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalars().first()
    if not resource:
        raise HTTPException(status_code=404, detail="Resource not found")
    resource.assigned_to = emergency_id
    resource.status = "DISPATCHED"
    await db.commit()
    return {"status": "Dispatched", "resource_id": resource_id, "emergency_id": emergency_id}

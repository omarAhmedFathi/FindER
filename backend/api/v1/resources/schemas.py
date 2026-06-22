from pydantic import BaseModel, UUID4
from typing import Optional
from api.v1.resources.models import ResourceType


class ResourceCreate(BaseModel):
    name: Optional[str] = None
    type: ResourceType
    location_lat: float
    location_lon: float
    status: str = "AVAILABLE"


class ResourceUpdate(BaseModel):
    status: Optional[str] = None
    assigned_to: Optional[UUID4] = None
    location_lat: Optional[float] = None
    location_lon: Optional[float] = None


class ResourceResponse(BaseModel):
    id: UUID4
    name: Optional[str] = None
    type: ResourceType
    status: str
    assigned_to: Optional[UUID4] = None
    location_lat: float
    location_lon: float

    class Config:
        from_attributes = True

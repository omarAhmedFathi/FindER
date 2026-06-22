from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from api.v1.emergencies.models import EmergencyStatus


class EmergencyCreate(BaseModel):
    location_lat: float
    location_lon: float
    description: Optional[str] = None
    severity: int = 3
    is_anonymous: bool = False


class EmergencyUpdate(BaseModel):
    status: Optional[EmergencyStatus] = None
    description: Optional[str] = None
    severity: Optional[int] = None


class EmergencyResponse(BaseModel):
    id: UUID4
    reporter_id: Optional[UUID4] = None
    status: EmergencyStatus
    location_lat: float
    location_lon: float
    description: Optional[str] = None
    severity: int
    detected_via_nlp: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

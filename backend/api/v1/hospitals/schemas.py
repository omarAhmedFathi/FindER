from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime


class HospitalCreate(BaseModel):
    name: str
    location_lat: float
    location_lon: float
    total_beds: int
    available_beds: int
    trauma_level: int


class HospitalUpdate(BaseModel):
    available_beds: Optional[int] = None
    total_beds: Optional[int] = None
    trauma_level: Optional[int] = None


class HospitalResponse(BaseModel):
    id: UUID4
    name: str
    location_lat: float
    location_lon: float
    total_beds: int
    available_beds: int
    trauma_level: int
    admin_id: Optional[UUID4] = None

    class Config:
        from_attributes = True

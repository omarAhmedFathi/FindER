from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/safety", tags=["safety"])

class SafetyStatus(BaseModel):
    user_id: str
    status: str
    last_known_location: Optional[str] = None

mock_safety_db = []

@router.post("/status")
async def update_status(status: SafetyStatus):
    mock_safety_db.append(status.dict())
    return {"message": "Status updated successfully", "data": status}

@router.get("/status/{user_id}")
async def get_status(user_id: str):
    for entry in mock_safety_db:
        if entry["user_id"] == user_id:
            return entry
    raise HTTPException(status_code=404, detail="User status not found")

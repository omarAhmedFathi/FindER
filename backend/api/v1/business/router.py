from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/business", tags=["business"])

class DonationPledge(BaseModel):
    business_name: str
    resource_type: str
    quantity: int
    is_verified: bool = False

mock_donations = []

@router.post("/pledge")
async def pledge_donation(pledge: DonationPledge):
    mock_donations.append(pledge.dict())
    return {"message": "Donation pledged successfully. Awaiting verification.", "data": pledge}

@router.get("/pledge")
async def get_pledges():
    return mock_donations

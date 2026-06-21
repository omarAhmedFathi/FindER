from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/moderation", tags=["moderation"])

class Report(BaseModel):
    item_id: str
    reason: str
    reported_by: str

mock_reports = []

@router.post("/report")
async def report_item(report: Report):
    mock_reports.append(report.dict())
    return {"message": "Item reported for moderation"}

@router.get("/reports")
async def get_reports():
    return mock_reports

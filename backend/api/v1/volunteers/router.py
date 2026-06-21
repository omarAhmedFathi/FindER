from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/volunteers", tags=["volunteers"])

class VolunteerTask(BaseModel):
    task_id: str
    title: str
    required_skill: str
    assigned_to: str = None
    status: str = "PENDING"

mock_tasks_db = []

@router.post("/tasks")
async def create_task(task: VolunteerTask):
    mock_tasks_db.append(task.dict())
    return {"message": "Task created", "data": task}

@router.get("/tasks")
async def get_tasks(skill: str = None):
    if skill:
        return [t for t in mock_tasks_db if t.get("required_skill") == skill]
    return mock_tasks_db

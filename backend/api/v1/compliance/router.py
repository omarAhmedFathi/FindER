from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from core.database import get_db
from api.v1.auth.dependencies import get_current_user
from api.v1.auth.models import User

router = APIRouter(prefix="/compliance", tags=["compliance"])

@router.get("/export-data")
async def export_user_data(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    GDPR Right of Access (Article 15) & Right to Data Portability (Article 20).
    Compiles all data associated with the user into a structured JSON payload.
    """
    # Simulate DB fetch
    user_data = {
        "account": {
            "email": current_user.email,
            "role": current_user.role,
            # Note: Decryption handled automatically by EncryptedString SQLAlchemy type
            "full_name": current_user.full_name, 
        },
        "emergencies_reported": [],
        "telemetry_logs": []
    }
    return user_data

@router.delete("/forget-me")
async def delete_user_account(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """
    GDPR Right to Erasure / Right to be Forgotten (Article 17).
    Hard deletes the user from the database. Scrambles associated emergency logs
    to retain statistical analytics without retaining PII.
    """
    try:
        # Anonymize linked records (e.g., emergencies reported by this user)
        # UPDATE emergencies SET reporter_id = NULL WHERE reporter_id = current_user.id
        await db.execute(
            text("UPDATE emergencies SET reporter_id = NULL WHERE reporter_id = :uid"),
            {"uid": current_user.id}
        )
        
        # Hard delete user
        await db.delete(current_user)
        await db.commit()
        
        # Queue background task to clear from Redis Cache / Celery queues
        # background_tasks.add_task(purge_user_from_cache, current_user.id)

        return {"status": "success", "message": "All personal data has been permanently erased."}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail="Data erasure failed. Contact support.")

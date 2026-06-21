import uuid
from sqlalchemy import Column, String, Boolean, DateTime, Enum as SAEnum
from sqlalchemy import UUID
from core.database import Base
from sqlalchemy.sql import func
import enum

class UserRole(str, enum.Enum):
    EMERGENCY_MANAGER = "EMERGENCY_MANAGER"
    FIRST_RESPONDER = "FIRST_RESPONDER"
    FIELD_MEDIC = "FIELD_MEDIC"
    HOSPITAL_ADMIN = "HOSPITAL_ADMIN"
    BYSTANDER = "BYSTANDER"

class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=False)
    role = Column(SAEnum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

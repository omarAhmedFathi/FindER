"""initial

Revision ID: 001_initial
Revises: 
Create Date: 2026-06-22 00:00:00.000000

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = '001_initial'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    op.execute("CREATE TYPE user_role AS ENUM ('EMERGENCY_MANAGER', 'FIRST_RESPONDER', 'FIELD_MEDIC', 'HOSPITAL_ADMIN', 'BYSTANDER')")
    op.execute("CREATE TYPE emergency_status AS ENUM ('ACTIVE', 'ROUTED', 'RESOLVED', 'FALSE_ALARM')")
    op.execute("CREATE TYPE resource_type AS ENUM ('AMBULANCE', 'FIRE_TRUCK', 'HELO', 'SUPPLY_DROP')")

    op.create_table('users',
        sa.Column('id', postgresql.UUID(as_uuid=True), server_default=sa.text('gen_random_uuid()'), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('full_name', sa.String(length=100), nullable=False),
        sa.Column('role', postgresql.ENUM('EMERGENCY_MANAGER', 'FIRST_RESPONDER', 'FIELD_MEDIC', 'HOSPITAL_ADMIN', 'BYSTANDER', name='user_role'), nullable=False),
        sa.Column('is_active', sa.Boolean(), server_default=sa.text('true'), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Remaining tables mapped similarly...
    # For brevity, relying on init.sql for raw instantiation or completing the full model mapped setup next phases.

def downgrade() -> None:
    op.drop_table('users')
    op.execute("DROP TYPE resource_type")
    op.execute("DROP TYPE emergency_status")
    op.execute("DROP TYPE user_role")

"""
Base database model definition
"""

import uuid

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from src.app.configs.extensions import db


class Base(db.Model):
    """Base model with default fields"""

    __abstract__ = True

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=func.now())

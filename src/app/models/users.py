"""
Database model definition for users
"""

from src.app.configs.extensions import db
from .base_model import Base


class Users(Base):
    """Model fields for users."""

    __tablename__ = "users"

    username = db.Column(db.String(20), index=True, nullable=False, unique=True)
    email = db.Column(db.String, index=True, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    last_login = db.Column(db.DateTime(timezone=True), nullable=True)

    password_reset_token = db.Column(db.String, nullable=True)
    password_reset_expires = db.Column(db.DateTime, nullable=True)

"""
Schema definition for resources related to user model
"""

from marshmallow import fields

from src.app.configs.extensions import ma
from src.app.models.users import Users
from src.app.utils.validations import (
    validate_email_format,
    validate_password_strength,
    validate_username,
)


class UserCreateSchema(ma.SQLAlchemySchema):
    """Marshmallow schema for user creation."""

    class Meta:
        models: Users

    username = fields.String(required=True, validate=[validate_username])
    email = fields.Email(required=True, validate=[validate_email_format])
    password = fields.String(required=True, validate=[validate_password_strength])


class UserSchema(ma.SQLAlchemySchema):
    """Marshmallow schema for users model with explicit field definitions."""

    class Meta:
        model = Users

    id = fields.UUID(dump_only=True)
    username = fields.String(required=True)
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True)

    is_active = fields.Boolean(dump_only=True, required=False)
    is_verified = fields.Boolean(dump_only=True, required=False)

    last_login = fields.DateTime(allow_none=True, dump_only=True)

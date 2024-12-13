"""
Base generic CRUD operations definitions.
"""

import uuid
from typing import Optional, Type
from flask_smorest import Blueprint, abort
from sqlalchemy.orm import DeclarativeMeta

from src.app.configs.extensions import db, ma


class BaseCRUDResource:
    """
    Base class for creating CRUD resources
    with standard flask-smorest blueprint implementation

    Requires subclasses to define:
    - model_class: Storage/database model
    - schema_class: Marshmallow schema for serialization
    - blueprint: flask-smorest blueprint
    - primary_key: Name of the primary key field (default: "id")
    """

    SchemaType = ma.SQLAlchemySchema
    model_class: Optional[Type[DeclarativeMeta]] = None
    schema_class: Optional[Type[SchemaType]] = None
    blueprint: Optional[Type[Blueprint]] = None
    primary_key = "id"

    @classmethod
    def validate_uuid(cls, value: str) -> uuid.UUID:
        """
        Validate and convert a string to a UUID object.

        Args:
            value (str): UUID string to validate.

        Returns:
            uuid.UUID: Validated UUID object.

        Raises:
            ValueError: If the value is not a valid UUID.
        """

        try:
            return uuid.UUID(value)
        except ValueError:
            abort(400, message=f"Invalid UUID format for {cls.primary_key}: {value}")

    @classmethod
    def list(cls):
        """
        List all resources

        Returns:
            List of all resources
        """

        resources = db.session.query(cls.model_class).all()

        return cls.schema_class(many=True).dump(resources)

    @classmethod
    def read(cls, resource_id: str):
        """
        Read a specific resource by ID

        Args:
            resource_id: Unique identifier of the resource

        Returns:
            Requested resource

        Raises:
            404 error if resource not found
        """

        validated_id = cls.validate_uuid(resource_id)

        resource = (
            db.session.query(cls.model_class)
            .filter_by(**{cls.primary_key: validated_id})
            .first()
        )

        if not resource:
            abort(
                404,
                message=f"{cls.model_class.__name__} with ID {resource_id} not found",
            )

        return cls.schema_class().dump(resource)

    @classmethod
    def create(cls, data):
        """
        Creates a new resource

        Args:
            data (dict): Resource data

        Returns:
            Created resource

        Raises:
            SQLAlchemyError: If database operation fails
        """

        try:
            validated_data = cls.schema_class().load(data)
            resource = cls.model_class(**validated_data)

            db.session.add(resource)
            db.session.commit()

            return cls.schema_class().dump(resource), 201
        except Exception as e:
            db.session.rollback()

            return {"error": "Unexpected Error", "details": str(e)}, 500

    @classmethod
    def delete(cls, resource_id: str):
        """
        Deletes user associated with the resource_id.

        Args:
            resource_id: Unique identifier of the resource

        Raises:
            ResourceNotFoundError: If requested id is not found
        """

        try:
            validated_uuid = cls.validate_uuid(resource_id)

            resource = (
                db.session.query(cls.model_class)
                .filter_by(**{cls.primary_key: validated_uuid})
                .first()
            )

            if not resource:
                abort(
                    404,
                    message=f"{cls.model_class.__name__} with ID {resource_id} not found",
                )

            db.session.delete(resource)
            db.session.commit()

            return {"message": f"Deleted user with ID {resource_id}"}, 200
        except Exception as e:
            db.session.rollback()

            # Log the full error for debugging
            print(f"Delete method error: {type(e).__name__} - {str(e)}")

            # If it's a known error type from flask_smorest, re-raise
            if hasattr(e, "code") and hasattr(e, "data"):
                raise

            return {"error": "Unexpected Error", "details": str(e)}, 500

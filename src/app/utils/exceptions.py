from typing import Type
from flask import Flask, jsonify
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import HTTPException


# Define custom exception classes for specific errors
class CustomException(Exception):
    """Base class for custom exceptions."""

    status_code = 400

    def __init__(self, message, status_code=None):
        super().__init__(message)
        if status_code is not None:
            self.status_code = status_code
        self.message = message

    def to_dict(self):
        return {"error": self.message}


class AuthenticationError(CustomException):
    """Exception for authentication errors."""

    status_code = 401


class AuthorizationError(CustomException):
    """Exception for authorization errors."""

    status_code = 403


class ResourceNotFoundError(CustomException):
    """Exception for resource not found errors."""

    status_code = 404


# Register error handlers in Flask
def register_error_handlers(app: Type[Flask]):
    @app.errorhandler(ValidationError)
    def handle_validation_error(error):
        """Handle marshmallow validation errors."""

        response = {"error": "Validation failed", "details": error.messages}

        return jsonify(response), 400

    @app.errorhandler(AuthenticationError)
    def handle_authentication_error(error):
        """Handle authentication errors."""

        response = {"error": error.message}

        return jsonify(response), error.status_code

    @app.errorhandler(AuthorizationError)
    def handle_authorization_error(error):
        """Handle authorization errors."""
        response = {"error": error.message}

        return jsonify(response), error.status_code

    @app.errorhandler(ResourceNotFoundError)
    def handle_resource_not_found_error(error):
        """Handle resource not found errors."""

        response = {"error": error.message}

        return jsonify(response), error.status_code

    @app.errorhandler(HTTPException)
    def handle_http_exception(error):
        """Handle default HTTP exceptions."""

        response = {"error": error.name, "description": error.description}

        return jsonify(response), error.code

    @app.errorhandler(Exception)
    def handle_general_exception(error):
        """Handle uncaught exceptions."""

        response = {"error": "Internal Server Error", "message": str(error)}

        return jsonify(response), 500

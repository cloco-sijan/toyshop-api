"""
Application Factory
"""

from typing import Type
from flask import Flask
from flask_smorest import Api

from src.app.configs.base import Config
from src.app.configs.extensions import db, jwt, ma, migrate
from src.app.configs.swagger import swagger_blp
from src.app.utils.exceptions import register_error_handlers


def create_app(config_class=Config):
    """Initialize application"""

    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config["PROPAGATE_EXCEPTIONS"] = True

    initialize_extensions(app)
    register_error_handlers(app)
    app.register_blueprint(swagger_blp(), url_prefix=Config.SWAGGER_URL)

    api = Api(app)
    register_endpoints(api)

    return app, api


def initialize_extensions(app: Type[Flask]):
    """Initialize default flask extensions"""

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)
    jwt.init_app(app)


# def register_error_handlers(app: Type[Flask]):
#     """Register custom error handlers."""

#     from werkzeug.exceptions import NotFound, Unauthorized, MethodNotAllowed, Conflict
#     from marshmallow import ValidationError
#     from src.app.utils.exceptions import (
#         handle_validation_error,
#         handle_not_found_error,
#         handle_unauthorized_error,
#         handle_method_not_allowed_error,
#         handle_conflict_error,
#         global_exception_handler,
#     )

#     # Validation Errors
#     app.register_error_handler(ValidationError, handle_validation_error)

#     # HTTP Errors
#     app.register_error_handler(NotFound, handle_not_found_error)
#     app.register_error_handler(Unauthorized, handle_unauthorized_error)
#     app.register_error_handler(MethodNotAllowed, handle_method_not_allowed_error)
#     app.register_error_handler(Conflict, handle_conflict_error)

#     # Catch-all for unhandled exceptions
#     app.register_error_handler(Exception, global_exception_handler)


def register_endpoints(api: Type[Api]):
    """Register API endpoints"""

    from src.app.resources.users import user_blp

    api.register_blueprint(user_blp)

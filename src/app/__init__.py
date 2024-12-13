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


def register_endpoints(api: Type[Api]):
    """Register API endpoints"""

    from src.app.resources.users import user_blp

    api.register_blueprint(user_blp)

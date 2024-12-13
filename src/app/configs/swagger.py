"""
Swagger UI configurations
"""

from flask_swagger_ui import get_swaggerui_blueprint

from src.app.configs.base import Config


def swagger_blp():
    swagger_blueprint = get_swaggerui_blueprint(
        base_url=Config.SWAGGER_URL,
        api_url=Config.API_URL,
        config={"app_name": Config.API_TITLE, "filter": True},
    )

    return swagger_blueprint

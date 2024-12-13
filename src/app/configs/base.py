"""
Base application level configurations.
"""

from os import environ
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Configuration variables"""

    # Application configurations
    SECRET_KEY = environ.get("SECRET_KEY", "dev-secret")
    DEBUG = environ.get("DEBUG", "False").lower() in ("true", "1", "yes")
    API_TITLE = environ.get("APP_NAME", "Toy Shop API")
    SWAGGER_URL = "/docs"
    API_URL = "/swagger.json"
    API_VERSION = "1.0.0"
    OPENAPI_VERSION = "3.0.3"
    ERROR_404_HELP: False

    # Database configurations
    SQLALCHEMY_DATABASE_URI = environ.get("DATABASE_URL", "sqlite://app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = DEBUG

    # JWT Configurations
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = 1200  # In seconds ~ 20 minutes
    JWT_REFRESH_TOKEN_EXPIRES = 3600  # In seconds ~ 60 minutes

    # Logging Configurations
    LOG_LEVEL = environ.get("LOG_LEVEL", "INFO")
    LOG_DIR = "logs"

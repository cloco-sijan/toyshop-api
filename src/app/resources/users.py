"""
API resources definition for user model
"""

from flask_smorest import Blueprint
from flask_bcrypt import generate_password_hash

from src.app.models.users import Users
from src.app.schemas.user import UserCreateSchema, UserSchema
from src.app.resources.base_resources import BaseCRUDResource

user_blp = Blueprint("users", __name__, description="User operations")


class UserResource(BaseCRUDResource):
    model_class = Users
    schema_class = UserSchema
    blueprint = user_blp

    @classmethod
    @user_blp.route("/users", methods=["GET"])
    @user_blp.response(200, UserSchema(many=True))
    def user_list():
        """Get all active users"""

        return UserResource.list()

    @classmethod
    @user_blp.route("/users/<id>", methods=["GET"])
    @user_blp.response(200, UserSchema)
    def get_user(id):
        """Get a specific user by id"""

        return UserResource.read(id)

    @classmethod
    @user_blp.route("/users", methods=["POST"])
    @user_blp.arguments(UserCreateSchema)
    @user_blp.response(201, UserSchema)
    def create_user(data):
        """Create a new user"""

        data = data.copy()

        if "password" in data:
            data["password"] = generate_password_hash(data["password"])

        return UserResource.create(data)

    @classmethod
    @user_blp.route("/users/<id>", methods=["DELETE"])
    @user_blp.response(200)
    def delete_user(id):
        """Deletes a user associated with id"""

        return UserResource.delete(id)

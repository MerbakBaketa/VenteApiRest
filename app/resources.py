from flask import request
from flask_restful import Resource
from marshmallow import ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.models import Comporter, db, Product, User, Client, Commande
from app.schemas import (
    ProductSchema,
    UserSchema,
    ClientSchema,
    CommandeSchema,
    ComporterSchema,
)

from utils_dev.generic_class import GenericCrudResource


# Create  all manual classes for User registration and login, and a protected resource
class UserRegisterResource(Resource):
    user_schema = UserSchema()

    def post(self):
        data = request.get_json(silent=True)
        if data is None:
            return {"message": "No JSON body provided"}, 400

        try:
            new_user_data = self.user_schema.load(data)
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        username = new_user_data.get("username")
        email = new_user_data.get("email")
        password = new_user_data.get("password")

        if not username or not email or not password:
            return {"message": "Missing required fields"}, 400

        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        new_user = User(
            username=username, email=email, password=generate_password_hash(password)
        )
        db.session.add(new_user)
        db.session.commit()

        return self.user_schema.dump(new_user), 201


class UserLoginResource(Resource):
    user_schema = UserSchema()

    def post(self):
        data = request.get_json(silent=True)
        if data is None:
            return {"message": "No JSON body provided"}, 400

        try:
            login_data = self.user_schema.load(data, partial=("email",))
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        username = login_data.get("username")
        password = login_data.get("password")

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            access_token = create_access_token(identity=str(user.id))
            return {"access_token": access_token}, 200

        return {"message": "Invalid credentials"}, 401


class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {"message": f"This is a protected resource : {current_user_id}"}, 200


class ProductResource(GenericCrudResource):
    model = Product
    key_field = "code"
    schema = ProductSchema
    database = db


class ClientResource(GenericCrudResource):
    model = Client
    key_field = "code_client"
    schema = ClientSchema
    database = db


class CommandeResource(GenericCrudResource):
    model = Commande
    key_field = "commande_code"
    schema = CommandeSchema
    database = db


class ComporterResource(GenericCrudResource):
    model = Comporter
    key_field = "id"
    schema = ComporterSchema
    database = db

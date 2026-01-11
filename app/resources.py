from flask import request
from flask_restful import Resource 
from marshmallow import ValidationError
from app.models import db, Product, User, Client
from app.shemas import ProductSchema, UserSchema, ClientSchema
from flask_jwt_extended import create_access_token ,jwt_required, get_jwt_identity

class UserRegisterResource(Resource):
    user_schema = UserSchema()

    def post(self):
        try:
            new_user_data = self.user_schema.load(request.get_json())
            username = new_user_data["username"]
            email = new_user_data["email"]
            password = new_user_data["password"]
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        if not username or not email or not password:
            return {"message": "Missing required fields"}, 400
        if User.query.filter_by(username=username).first():
            return {"message": "Username already exists"}, 400

        new_user = User(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return self.user_schema.dump(new_user), 201

class UserLoginResource(Resource):
    user_schema = UserSchema()
    def post(self):
        try:
            login_data = self.user_schema.load(request.get_json(), partial=("email",))
            username = login_data.get("username")
            password = login_data.get("password")
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            acces_token= create_access_token(identity=str(user.id))
            return { "access_token": acces_token}, 200
        return {"message": "Invalid credentials"}, 401

class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        return {"message": f"This is a protected resource : {current_user_id}"}, 200
class ProductListResource(Resource):
    product_schema = ProductSchema()
    product_list_schema = ProductSchema(many=True)
    product_patch_schema = ProductSchema(partial=True)

    def get(self, product_id=None):
        if product_id:
            product = Product.query.get(product_id)
            return self.product_schema.dump(product)
        else:
            products = Product.query.all()
            return self.product_list_schema.dump(products)

    def post(self):
        try:
            new_product_data = self.product_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        new_product = Product(
            code=new_product_data["code"],
            name=new_product_data["name"],
            prix=new_product_data["prix"],
            qte=new_product_data["qte"],
            categorie=new_product_data["categorie"],
        )
        db.session.add(new_product)
        db.session.commit()

        return self.product_schema.dump(new_product), 201

    def put(self, product_id):
        try:
            new_product_data = self.product_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        product = Product.query.get_or_404(product_id)

        for key, value in new_product_data.items():
            if value is not None:
                setattr(product, key, value)

        db.session.commit()
        return self.product_schema.dump(product), 200

    def patch(self, product_id):
        try:
            new_product_data = self.product_patch_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        product = Product.query.get_or_404(product_id)

        for key, value in new_product_data.items():
            if value is not None:
                setattr(product, key, value)

        db.session.commit()
        return self.product_patch_schema.dump(product), 200

    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return "", 204

class clientListResource(Resource):
    client_schema = ClientSchema()
    client_list_schema = ClientSchema(many=True)
    client_patch_schema = ClientSchema(partial=True)

    def get(self, client_id=None):
        if client_id:
            client = Client.query.get(client_id)
            return self.client_schema.dump(client)
        else:
            clients = Client.query.all()
            return self.client_list_schema.dump(clients)

    def post(self):
        try:
            new_client_data = self.client_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400
        new_client = Client(
            code_client=new_client_data["code_client"],
            nom=new_client_data["nom"],
            email=new_client_data["email"],
            telephone=new_client_data["telephone"],
        )
        db.session.add(new_client)
        db.session.commit()

        return self.client_schema.dump(new_client), 201

    def put(self, client_id):
        try:
            new_client_data = self.client_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        client = Client.query.get_or_404(client_id)

        for key, value in new_client_data.items():
            if value is not None:
                setattr(client, key, value)

        db.session.commit()
        return self.client_schema.dump(client), 200

    def patch(self, client_id):
        try:
            new_client_data = self.client_patch_schema.load(request.get_json())
        except ValidationError as err:
            return {"message": "Validation error", "errors": err.messages}, 400

        client = Client.query.get_or_404(client_id)

        for key, value in new_client_data.items():
            if value is not None:
                setattr(client, key, value)

        db.session.commit()
        return self.client_patch_schema.dump(client), 200

    def delete(self, client_id):
        client = Client.query.get_or_404(client_id)
        db.session.delete(client)
        db.session.commit()
        return "", 204

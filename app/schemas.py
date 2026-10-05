from flask_marshmallow import Marshmallow
from app.models import User, Product, Client, Commande, Comporter, db

ma = Marshmallow()


class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = False
        sqla_session = db.session


class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = False
        sqla_session = db.session


class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = True
        sqla_session = db.session


class CommandeSchema(ma.SQLAlchemyAutoSchema):

    client = ma.Nested(ClientSchema, many=False)
    lignes_commande = ma.Nested("ComporterSchema", many=True)

    class Meta:
        model = Commande
        include_fk = True
        load_instance = True
        sqla_session = db.session


class ComporterSchema(ma.SQLAlchemyAutoSchema):
    produit = ma.Nested(ProductSchema, many=False)

    class Meta:
        model = Comporter
        include_fk = True
        load_instance = True
        sqla_session = db.session

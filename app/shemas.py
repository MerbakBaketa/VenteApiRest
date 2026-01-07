from flask_marshmallow import Marshmallow
from app.models import Product, Client, Commande, Comporter, db

ma = Marshmallow()

class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Product
        load_instance = False
        sqla_session = db.session

class ClientSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Client
        load_instance = False
        sqla_session = db.session

class CommandeSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Commande
        load_instance = False
        sqla_session = db.session

class ComporterSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Comporter
        load_instance = False
        sqla_session = db.session
from flask import request
from flask_restful import Resource, Api
from marshmallow import ValidationError
from app.models import db, Product
from app.shemas import ProductSchema

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
            code=new_product_data['code'],
            name=new_product_data['name'],
            prix=new_product_data['prix'],
            qte=new_product_data['qte'],
            categorie=new_product_data['categorie']
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
        
        for key,value in new_product_data.items():
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
        
        for key,value in new_product_data.items():
            if value is not None:
                setattr(product, key, value)

        db.session.commit()
        return self.product_patch_schema.dump(product), 200
    
    def delete(self, product_id):
        product = Product.query.get_or_404(product_id)
        db.session.delete(product)
        db.session.commit()
        return '', 204
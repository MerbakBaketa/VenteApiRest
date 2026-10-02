from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

class GenericCrudResource(Resource):
    schema = None
    database = None

    def get_json_data(self):
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return None
        return data

    def _get_schema(self, EntitySchema=None, many=False):
        schema_class = EntitySchema or self.schema
        if schema_class is None:
            raise ValueError("Aucun schéma fourni.")

        if many:
            return schema_class(many=True)
        return schema_class()

    def get(self, key_field=None, EntitySchema=None, Entity_list_schema=None, model=None):
        model = model or self.model
        if model is None:
            return {"message": "Model not provided"}, 500

        if key_field:
            instance = model.query.get_or_404(key_field)
            schema = self._get_schema(EntitySchema)
            return schema.dump(instance)

        schema = self._get_schema(Entity_list_schema, many=True)
        items = model.query.all()
        return schema.dump(items)

    def post(self, EntitySchema=None, model=None, database=None):
        model = model or self.model
        database = database or self.database
        if model is None:
            return {"message": "Model not provided"}, 500

        json_data = self.get_json_data()
        if json_data is None:
            return {"message": "No JSON body provided"}, 400

        schema = self._get_schema(EntitySchema)

        try:
            new_data = schema.load(json_data)
            model_instance = model(**new_data)
            database.session.add(model_instance)
            database.session.commit()
            return schema.dump(model_instance), 201

        except ValidationError as err:
            database.session.rollback()
            return {"message": "Validation error", "errors": err.messages}, 400

        except Exception as err:
            database.session.rollback()
            return {"message": "Database error", "error": str(err)}, 500

    def put(self, key_field, EntitySchema=None, model=None, database=None):
        model = model or self.model
        database = database or self.database
        if model is None:
            return {"message": "Model not provided"}, 500

        json_data = self.get_json_data()
        if json_data is None:
            return {"message": "No JSON body provided"}, 400

        schema = self._get_schema(EntitySchema)

        try:
            new_data = schema.load(json_data)
            instance = model.query.get_or_404(key_field)

            for key, value in new_data.items():
                if value is not None:
                    setattr(instance, key, value)

            database.session.commit()
            return schema.dump(instance), 200

        except ValidationError as err:
            database.session.rollback()
            return {"message": "Validation error", "errors": err.messages}, 400

        except Exception as err:
            database.session.rollback()
            return {"message": "Database error", "error": str(err)}, 500

    def patch(self, key_field, EntitySchema=None, model=None, database=None):
        model = model or self.model
        database = database or self.database
        if model is None:
            return {"message": "Model not provided"}, 500

        json_data = self.get_json_data()
        if json_data is None:
            return {"message": "No JSON body provided"}, 400

        schema = self._get_schema(EntitySchema)

        try:
            new_data = schema.load(json_data, partial=True)
            instance = model.query.get_or_404(key_field)

            for key, value in new_data.items():
                if value is not None:
                    setattr(instance, key, value)

            database.session.commit()
            return schema.dump(instance), 200

        except ValidationError as err:
            database.session.rollback()
            return {"message": "Validation error", "errors": err.messages}, 400

        except Exception as err:
            database.session.rollback()
            return {"message": "Database error", "error": str(err)}, 500

    def delete(self, key_field, database=None, model=None):
        model = model or self.model
        database = database or self.database
        if model is None:
            return {"message": "Model not provided"}, 500

        try:
            instance = model.query.get_or_404(key_field)
            database.session.delete(instance)
            database.session.commit()
            return "", 204

        except Exception as err:
            database.session.rollback()
            return {"message": "Database error", "error": str(err)}, 500
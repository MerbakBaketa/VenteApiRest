from flask_jwt_extended import jwt_required, get_jwt
from functools import wraps
from flask import jsonify
from flask_restful import Resource


def role_required(allowed_roles, key_role="role"):
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get(key_role) not in allowed_roles:
                return jsonify({"error": "Accès refusé"}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator

class RoleProtectedResource(Resource):
    allowed_roles = []
    method_decorators = []

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if cls.allowed_roles:
            cls.method_decorators = [role_required(cls.allowed_roles)]

    @jwt_required()
    def get(self):
        data_jwt = get_jwt()
        username = data_jwt.get("username")
        role = data_jwt.get("role")
        return {"message": f"Accès autorisé à {username} avec rôle {role}"}, 200
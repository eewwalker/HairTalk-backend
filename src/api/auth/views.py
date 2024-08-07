from flask import request, jsonify
from flask_restx import Resource, Namespace
from flask_bcrypt import Bcrypt
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.api.users.models import User
from ..users.crud import read_users, create_user
from ..users.views import user_model


bcrypt = Bcrypt()

auth_namespace = Namespace('auth')

class Register(Resource):
    @auth_namespace.expect(user_model, validate=True)
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')
            location = data.get('location')

            users = read_users()
            if any(user.username == username for user in users):
                return {'message': 'User already exists'}, 400

            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            create_user(username=username, password=hashed_password, location=location)
            return {'message': f'User:{username} registered'}, 201

        except ValueError as e:
            return {'message': str(e)}, 500
        except Exception as e:
            return {'message': f"An unexpected error occurred: {e}"}, 500


class Login(Resource):
    @auth_namespace.expect(user_model, validate=True)
    def post(self):
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            user = User.query.filter_by(username=username).first()
            if not user or not bcrypt.check_password_hash(user.password, password):
                return {'message': 'Invalid credentials'}, 401

            response_data = {
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'location': user.location
                }
            }

            return jsonify(response_data), 200

        except ValueError as e:
            return {'message': str(e)}, 500
        except Exception as e:
            return {'message': f"An unexpected error occurred: {e}"}, 500


class Protected(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            return {'logged_in_as': current_user}, 200
        except Exception as e:
            return {'message': f'An unexpected error occurred: {e}'}, 500

class VerifyToken(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user = get_jwt_identity()
            return {'logged_in_as': current_user}, 200
        except Exception as e:
            return {'message': f'An unexpected error occurred: {e}'}, 500

auth_namespace.add_resource(Register, '/register')
auth_namespace.add_resource(Login, '/login')
auth_namespace.add_resource(Protected, '/protected')
auth_namespace.add_resource(VerifyToken, '/verify_token')
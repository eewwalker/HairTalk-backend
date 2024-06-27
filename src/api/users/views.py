from urllib import request
from flask_restx import Namespace, Resource, fields
from .crud import read_users, read_user, create_user
users_namespace = Namespace('users')

user_model = users_namespace.model('User',{
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True, description='Name of the user', example="John Doe"),
    'location': fields.String()
})

class UserList(Resource):
    @users_namespace.marshal_list_with(user_model)
    def get(self):
        try:
            users = read_users()
            return users, 200
        except ValueError as e:
            users_namespace.abort(500, str(e))

    @users_namespace.expect(user_model, validate=True)
    @users_namespace.marshal_with(user_model, code=201)
    def post(self):
        try:
            data = request.get_json()
            name = data['name']
            location = data['location']
            user = create_user(name=name, location=location)
            return user, 201
        except ValueError as e:
            users_namespace.abort(400, str(e))
        except KeyError as e:
            users_namespace.abort(400, f"Missing field: {e}")
        except Exception as e:
            users_namespace.abort(500, str(e))

users_namespace.add_resource(UserList, '/')

class UserResource(Resource):
    @users_namespace.marshal_with(user_model)
    def get(self, id):
        try:
            user = read_user(id)
            if user:
                return user, 200
            else:
                users_namespace.abort(404, f"User id:{id} not found")
        except ValueError as e:
            users_namespace.abort(500, str(e))

users_namespace.add_resource(UserResource, '/<int:id>')



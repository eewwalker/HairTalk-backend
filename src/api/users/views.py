from flask_restx import Namespace, Resource, fields
from .crud import read_users
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

users_namespace.add_resource(UserList, '/')

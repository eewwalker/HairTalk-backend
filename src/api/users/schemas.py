from flask_restx import Namespace, fields

users_namespace = Namespace('users')


user_model = users_namespace.model('User', {
    'id': fields.String(readOnly=True,
                        attribute=lambda x: str(x.id) if x.id else None,
                        description='User UUID',
                        example='91014f8a-e002-497c-b6e5-5fdd7e4d9787'),
    'username': fields.String(required=True, description='Username for user', example="John Doe"),
    'password': fields.String(required=True, description='Password for user'),
    'location': fields.String()
})

update_user_model = users_namespace.model('User',{
    'username': fields.String(description='Username for user', example="John Doe"),
    'location': fields.String()
})
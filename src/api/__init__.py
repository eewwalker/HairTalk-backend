from flask_restx import Api

from src.api.ping import ping_namespace
from src.api.users.views import users_namespace
from src.api.questions.views import questions_namespace

api = Api(version="1.0", title="Users API", doc="/doc")

api.add_namespace(ping_namespace, path="/ping")
api.add_namespace(users_namespace, path="/users")
api.add_namespace(questions_namespace, path="/questions")


from flask import Flask, request
from flask_restx import Namespace, Resource, fields
from .crud import create_question, read_question, read_questions, read_conversation

questions_namespace = Namespace('questions')

question_model = questions_namespace.model('Question', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.Integer(required=True, description='Id attached to user', example="1"),
    'content': fields.String(),
    'created_at': fields.Date()
})

conversation_model = questions_namespace.model('Conversation', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.Integer,
    'content': fields.String,
    'created_at': fields.DateTime,
    'answers': fields.List(fields.Nested(questions_namespace.model('Answer', {
        'id': fields.Integer,
        'user_id': fields.Integer,
        'content': fields.String,
        'created_at': fields.DateTime,
        'comments': fields.List(fields.Nested(questions_namespace.model('Comment', {
            'id': fields.Integer,
            'user_id': fields.Integer,
            'content': fields.String,
            'created_at': fields.DateTime
        })))
    })))
})


class QuestionList(Resource):
    @questions_namespace.marshal_list_with(question_model)
    def get(self):
        try:
            questions = read_questions()
            return questions, 200
        except ValueError as e:
            questions_namespace.abort(500, str(e))

    @questions_namespace.expect(question_model, validate=True)
    @questions_namespace.marshal_with(question_model, code=201)
    def post(self):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            content = data.get('content')
            created_at = data.get('created_at')
            question = create_question(
                user_id=user_id,
                content=content,
                created_at=created_at
            )
            return question, 201
        except ValueError as e:
            questions_namespace.abort(400, str(e))
        except KeyError as e:
            questions_namespace.abort(400, f"Missing field: {e}")
        except Exception as e:
            questions_namespace.abort(500, str(e))


class QuestionResource(Resource):
    @questions_namespace.marshal_list_with(question_model)
    def get(self, id):
        try:
            question = read_question(id)
            if question:
                return question, 200
            else:
                questions_namespace.abort(404, f"User id:{id} not found")
        except ValueError as e:
            questions_namespace.abort(500, str(e))


class ConversationResource(Resource):
    @questions_namespace.marshal_with(conversation_model)
    def get(self, question_id):
        try:
            conversation = read_conversation(question_id)
            print('conversation', conversation)
            if conversation:
                return conversation, 200
            else:
                questions_namespace.abort(
                    404, f"Question with id {question_id} not found")
        except ValueError as e:
            questions_namespace.abort(500, str(e))


questions_namespace.add_resource(QuestionList, '/')
questions_namespace.add_resource(QuestionResource, '/<int:id>')
questions_namespace.add_resource(
    ConversationResource, '/<int:question_id>/conversation')

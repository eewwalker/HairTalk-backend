from flask_restx import Namespace, fields

questions_namespace = Namespace('questions')

question_model = questions_namespace.model('Question', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(),
    'user_id': fields.Integer(required=True, description='Id attached to user', example="1"),
    'content': fields.String(),
    'created_at': fields.Date()
})

answer_model_marshal = questions_namespace.model('Answer', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.Integer(required=True, description='Id attached to user', example="1"),
    'question_id': fields.Integer(required=True, description='Id of the associated question', example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

answer_model_validate = questions_namespace.model('Answer', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.Integer(required=True, description='Id attached to user', example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

comment_model_marshal = questions_namespace.model('Comment', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.Integer(required=True, description='Id attached to user', example="1"),
    'answer_id': fields.Integer(required=True, description='Id of the associated answer', example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

comment_model_validate = questions_namespace.model('Comment', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.Integer(required=True, description='Id attached to user', example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
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

from flask_restx import Namespace, fields

questions_namespace = Namespace('questions')

question_model = questions_namespace.model('Question', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(),
    'user_id': fields.String(required=True, description='UUID attached to user', example="123e4567-e89b-12d3-a456-426614174000"),
    'content': fields.String(),
    'created_at': fields.Date()
})

pagination_model = questions_namespace.model('PaginatedQuestion', {
    'items': fields.List(fields.Nested(question_model)),
    'total': fields.Integer,
    'pages': fields.Integer,
    'current_page': fields.Integer
} )

answer_model_marshal = questions_namespace.model('Answer', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.String(required=True, description='UUID attached to user', example="123e4567-e89b-12d3-a456-426614174000"),
    'question_id': fields.Integer(required=True, description='Id of the associated question', example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

answer_model_validate = questions_namespace.model('Answer', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.String(required=True, description='UUID attached to user', example="123e4567-e89b-12d3-a456-426614174000"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

comment_model_marshal = questions_namespace.model('Comment', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.String(required=True, description='UUID attached to user', example="123e4567-e89b-12d3-a456-426614174000"),
    'answer_id': fields.Integer(required=True, description='Id of the associated answer', example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

comment_model_validate = questions_namespace.model('Comment', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.String(required=True, description='UUID attached to user', example="123e4567-e89b-12d3-a456-426614174000"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

conversation_model = questions_namespace.model('Conversation', {
    'id': fields.Integer(readOnly=True),
    'user_id': fields.String,
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

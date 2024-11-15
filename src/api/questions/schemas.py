from flask_restx import Namespace, fields

questions_namespace = Namespace('questions')

tag_model = questions_namespace.model('Tag', {
    'id': fields.Integer(readOnly=True),
    'name': fields.String(required=True,
                          description='Tag name',
                          example='hair-color')
})

question_create_model = questions_namespace.model('QuestionCreate', {

    'userId': fields.String(required=True,
                            attribute='user_id',
                            description='UUID attached to user',
                            example="123e4567-e89b-12d3-a456-426614174000"),
    'title': fields.String(required=True,
                           description='Question title',
                           example='How to fix brassy highlights?'),
    'content': fields.String(required=True,
                             description='Question content',
                             example='My highlights are turning brassy...'),
    'tags': fields.List(fields.String(),
                        attribute='tags_list',
                        description='List of tag names',
                        example=['color-correction', 'highlights'],
                        required=False,
                        default=[])
})

question_response_model = questions_namespace.model('QuestionResponse', {
    'id': fields.Integer(readOnly=True),
    'title': fields.String(required=True,
                           description='Question title',
                           example='How to fix brassy highlights?'),
    'content': fields.String(required=True,
                             description='Question content',
                             example='My highlights are turning brassy...'),
    'userId': fields.String(required=True,
                            attribute='user_id',
                            description='UUID attached to user',
                            example="123e4567-e89b-12d3-a456-426614174000"),
    'author_username': fields.String(required=True),
    'created_at': fields.Date(readOnly=True),
    'tags': fields.List(fields.String(),
                        attribute='tags_list',
                        description='List of tag names',
                        example=['color-correction', 'highlights'],
                        required=False)
})

pagination_model = questions_namespace.model('PaginatedQuestion', {
    'items': fields.List(fields.Nested(question_response_model)),
    'total': fields.Integer,
    'pages': fields.Integer,
    'current_page': fields.Integer
} )

answer_model_marshal = questions_namespace.model('Answer', {
    'id': fields.Integer(readOnly=True),
    'userId': fields.String(required=True,
                            description='UUID attached to user',
                            example="123e4567-e89b-12d3-a456-426614174000"),
    'question_id': fields.Integer(required=True,
                                  description='Id of the associated question',
                                  example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

answer_model_validate = questions_namespace.model('Answer', {
    'id': fields.Integer(readOnly=True),
    'userId': fields.String(required=True,
                            description='UUID attached to user',
                            example="123e4567-e89b-12d3-a456-426614174000"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

comment_model_marshal = questions_namespace.model('Comment', {
    'id': fields.Integer(readOnly=True),
    'userId': fields.String(required=True,
                            description='UUID attached to user',
                            example="123e4567-e89b-12d3-a456-426614174000"),
    'answer_id': fields.Integer(required=True,
                                description='Id of the associated answer',
                                example="1"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

comment_model_validate = questions_namespace.model('Comment', {
    'id': fields.Integer(readOnly=True),
    'userId': fields.String(required=True,
                            description='UUID attached to user',
                            example="123e4567-e89b-12d3-a456-426614174000"),
    'content': fields.String(),
    'created_at': fields.DateTime()
})

conversation_model = questions_namespace.model('Conversation', {
    'id': fields.Integer(readOnly=True),
    'userId': fields.String,
    'content': fields.String,
    'created_at': fields.DateTime,
    'answers': fields.List(fields.Nested(questions_namespace.model('Answer', {
        'id': fields.Integer,
        'userId': fields.Integer,
        'content': fields.String,
        'created_at': fields.DateTime,
        'comments': fields.List(fields.Nested(questions_namespace.model('Comment', {
            'id': fields.Integer,
            'userId': fields.Integer,
            'content': fields.String,
            'created_at': fields.DateTime
        })))
    })))
})

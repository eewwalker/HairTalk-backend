from flask import request
from flask_restx import Resource, reqparse
from .crud import (create_question, read_question, read_questions,
                   read_conversation, create_answer, create_comment)
from .schemas import (questions_namespace, question_create_model,
                      question_response_model, answer_model_marshal,
                      answer_model_validate,
                      comment_model_marshal, comment_model_validate,
                      conversation_model, pagination_model)
from ...utils.uuid_utils import parse_uuid
class QuestionList(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('page', type=int, default=1, help='Page number')
    parser.add_argument('per_page', type=int,
                        default=15, help="Items per page")

    @questions_namespace.marshal_list_with(pagination_model)
    def get(self):
        args = self.parser.parse_args()
        page = args['page']
        per_page = args['per_page']

        try:
            questions = read_questions(page=page, per_page=per_page)

            return questions, 200

        except ValueError as e:
            questions_namespace.abort(500, str(e))

    @questions_namespace.expect(question_create_model, validate=True)
    @questions_namespace.marshal_with(question_response_model, code=201)
    def post(self):
        print("Received request") # Debug log
        try:
            data = request.get_json()
            print("Request data:", data) # Debug log

            question = create_question(
                user_id=parse_uuid(data.get('userId')),
                title=data.get('title'),
                content=data.get('content'),
                tag_names=data.get('tags', [])
            )

            return question, 201
        except ValueError as e:
            questions_namespace.abort(400, str(e))
        except KeyError as e:
            questions_namespace.abort(400, f"Missing field: {e}")
        except Exception as e:
            questions_namespace.abort(500, str(e))


class QuestionResource(Resource):
    @questions_namespace.marshal_with(question_response_model)
    def get(self, id):
        try:
            question = read_question(id)
            if question:
                return question, 200
            else:
                questions_namespace.abort(
                    404, f"Question with id {id} not found")
        except ValueError as e:
            questions_namespace.abort(500, str(e))


class ConversationResource(Resource):
    @questions_namespace.marshal_with(conversation_model)
    def get(self, question_id):
        try:
            conversation = read_conversation(question_id)
            if conversation:
                return conversation, 200
            else:
                questions_namespace.abort(
                    404, f"Question with id {id} not found")
        except ValueError as e:
            questions_namespace.abort(500, str(e))


class AnswerList(Resource):
    @questions_namespace.expect(answer_model_validate, validate=True)
    @questions_namespace.marshal_with(answer_model_marshal, code=201)
    def post(self, question_id):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            content = data.get('content')
            answer = create_answer(
                user_id=user_id,
                question_id=question_id,
                content=content
            )
            return answer, 201
        except ValueError as e:
            questions_namespace.abort(400, str(e))
        except KeyError as e:
            questions_namespace.abort(400, f"Missing field: {e}")
        except Exception as e:
            questions_namespace.abort(500, str(e))


class CommentList(Resource):
    @questions_namespace.expect(comment_model_validate, validate=True)
    @questions_namespace.marshal_with(comment_model_marshal, code=201)
    def post(self, question_id, answer_id):
        try:
            data = request.get_json()
            user_id = data.get('user_id')
            answer_id = answer_id
            content = data.get('content')
            comment = create_comment(
                user_id=user_id,
                answer_id=answer_id,
                content=content
            )
            return comment, 201
        except ValueError as e:
            questions_namespace.abort(400, str(e))
        except KeyError as e:
            questions_namespace.abort(400, f"Missing field: {e}")
        except Exception as e:
            questions_namespace.abort(500, str(e))


questions_namespace.add_resource(QuestionList, '/')
questions_namespace.add_resource(QuestionResource, '/<int:id>')
questions_namespace.add_resource(
    ConversationResource, '/<int:question_id>/conversation')
questions_namespace.add_resource(AnswerList, '/<int:question_id>/answers')
questions_namespace.add_resource(
    CommentList, '/<int:question_id>/answers/<int:answer_id>/comments')

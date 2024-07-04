from flask import request
from flask_restx import Resource
from .crud import (create_question, read_question, read_questions,
                   read_conversation, create_answer, create_comment)
from .schemas import (questions_namespace, question_model, answer_model_marshal, answer_model_validate,
                      comment_model_marshal, comment_model_validate, conversation_model)


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
    @questions_namespace.marshal_with(question_model)
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

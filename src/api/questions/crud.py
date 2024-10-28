from src import db
# from sqlalchemy.exc import IntegrityError
from .models import Question, Answer, Comment, Tag
from sqlalchemy import desc

def get_or_create_tags(tag_names):
    tags = []
    for name in tag_names:
        tag = Tag.query.filter_by(name=name).first()
        if not tag:
            tag = Tag(name=name)
            db.session.add(tag)
        tags.append(tag)
    return tags


def create_question(user_id, title, content, created_at, tag_names=None):
    try:
        question = Question(user_id=user_id, title=title, content=content)
        if tag_names:
            tags = get_or_create_tags(tag_names)
            question.tags.extend(tags) # Adds the Tags to this Question

        db.session.add(question)
        db.session.commit()
        return question
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating question: {e}")


def create_answer(user_id, question_id, content):
    try:
        answer = Answer(user_id=user_id,
                        question_id=question_id, content=content)
        db.session.add(answer)
        db.session.commit()
        return answer
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating answer: {e}")


def create_comment(user_id, answer_id, content):
    try:
        comment = Comment(
            user_id=user_id, answer_id=answer_id, content=content)
        db.session.add(comment)
        db.session.commit()
        return comment
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating comment: {e}")


def read_question(id):
    try:
        return Question.query.filter(Question.id == id).first()
    except Exception as e:
        raise ValueError(f"Error reading question {id}: {e}")


def read_questions(page=1, per_page=20):
    try:
        return Question.query.order_by(desc(Question.created_at)).\
                        paginate(page=page, per_page=per_page, error_out=False)
    except Exception as e:
        raise ValueError(f"Error reading questions: {e}")


def read_conversation(question_id):
    try:
        question = Question.query.filter_by(id=question_id).first()
        if not question:
            return None

        answers = Answer.query.filter_by(question_id=question.id).all()
        conversation = {
            "id": question.id,
            "user_id": question.user_id,
            "content": question.content,
            "created_at": question.created_at,
            "answers": []
        }

        for answer in answers:
            comments = Comment.query.filter_by(answer_id=answer.id).all()
            answer_data = {
                "id": answer.id,
                "user_id": answer.user_id,
                "content": answer.content,
                "created_at": answer.created_at,
                "comments": []
            }
            for comment in comments:
                comment_data = {
                    "id": comment.id,
                    "user_id": comment.user_id,
                    "content": comment.content,
                    "created_at": comment.created_at
                }
                answer_data["comments"].append(comment_data)

            conversation["answers"].append(answer_data)

        return conversation
    except Exception as e:
        db.session.rollback()
        raise ValueError(
            f"Error fetching conversation for question {question_id}: {e}")

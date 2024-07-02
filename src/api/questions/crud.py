from src import db
from sqlalchemy.exc import IntegrityError
from .models import Question

def create_question(user_id, content, created_at):
    try:
        question = Question(user_id=user_id, content=content, created_at=created_at)
        db.session.add(question)
        db.session.commit()
        return question
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating question: {e}")


def read_question(id):
    try:
        return Question.query.filter(Question.id == id).first()
    except Exception as e:
        raise ValueError(f"Error reading question {id}: {e}")

def read_questions():
    try:
        return Question.query.all()
    except Exception as e:
        raise ValueError(f"Error reading questions: {e}")


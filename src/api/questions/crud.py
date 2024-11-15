from src import db
# from sqlalchemy.exc import IntegrityError
from .models import Question, Answer, Comment, Tag
from sqlalchemy import desc
from ..users.models import User

def get_or_create_tags(tag_names):
    """
    Get existing tags or create new tags
    Args:
        tag_names(str[])
    Returns:
        list of Tag objs
    """
    tags = []
    for name in tag_names:
        normalize_name = name.strip().lower()
        if normalize_name:
            tag = Tag.query.filter_by(name=normalize_name).first()
            if not tag:
                tag = Tag(name=normalize_name)
                db.session.add(tag)
            tags.append(tag)
    return tags

def create_question(user_id, title, content, tag_names=None):
    """
    Create a new question with optional tags
    Args:
        user_id(UUID), title(str), content(str), tag_names(str[])
    Returns:
        question object
    Raises:
        ValueError if error creating question
    """
    try:
        user = User.query.get(user_id)
        if not user:
            raise ValueError(f"User with id {user_id} does not exist")

        # Create new question
        question = Question(user_id=user_id, title=title, content=content)

        # Handle tags if submitted
        if tag_names:
            # filter out empty strings and duplicates
            tag_names = list(set(filter(None, tag_names)))
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


def read_questions(page=1, per_page=15):
    try:
        questions = Question.query\
            .join(User)\
            .options(db.joinedload(Question.user))\
            .order_by(desc(Question.created_at))\
            .paginate(page=page, per_page=per_page, error_out=False)
        # return Question.query.order_by(desc(Question.created_at)).\
        #                 paginate(page=page, per_page=per_page, error_out=False)
        return {
            'items': [
                {
                    'id': q.id,
                    'title': q.title,
                    'content': q.content,
                    'user_id': str(q.user_id),
                    'author_username': q.user.username,
                    'created_at': q.created_at.strftime('%Y-%m-%d'),
                    'tags': q.tags_list
                } for q in questions.items
            ],
            'total': questions.total,
            'pages': questions.pages,
            'current_page': questions.page
        }
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

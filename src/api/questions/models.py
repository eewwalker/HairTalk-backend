from sqlalchemy.dialects.postgresql import UUID
from src import db
from datetime import datetime

# Association table for the many-to-many relationship between Question and Tag
question_tags = db.Table('question_tags',
    db.Column('question_id', db.Integer, db.ForeignKey('questions.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)
class Tag(db.Model):
    __tablename__= "tags"

    id = db.Column(
        db.Integer(),
        primary_key=True
    )

    name = db.Column(
        db.Text,
        unique=True,
        nullable=False
    )

    def __init__(self, name):
        self.name=name

class Question(db.Model):
    __tablename__ = "questions"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.id'),
        nullable=False
    )

    title = db.Column(
        db.Text,
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        nullable=False
    )

    tags = db.relationship('Tag', secondary=question_tags, backref=db.backref('questions', lazy='dynamic'))

    def __init__(self, user_id, title, content, created_at=None):
        self.user_id = user_id
        self.title = title
        self.content = content
        self.created_at = created_at if created_at else datetime.now()


class Answer(db.Model):
    __tablename__ = "answers"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.id'),
        nullable=False)

    question_id = db.Column(
        db.Integer,
        db.ForeignKey('questions.id'),
        nullable=False)

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
    )

    question = db.relationship(
        'Question',
        backref=db.backref('answers', lazy=True)
    )

    def __init__(self, user_id, question_id, content, created_at=None):
        self.user_id = user_id
        self.question_id = question_id
        self.content = content
        self.created_at = created_at if created_at else datetime.now()


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        UUID(as_uuid=True),
        db.ForeignKey('users.id'),
        nullable=False
    )

    answer_id = db.Column(
        db.Integer,
        db.ForeignKey('answers.id'),
        nullable=False
    )

    content = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
    )

    def __init__(self, user_id, answer_id, content, created_at=None):
        self.user_id = user_id
        self.answer_id = answer_id
        self.content = content
        self.created_at = created_at if created_at else datetime.now()





from src import db
from datetime import datetime


class Question(db.Model):
    __tablename__= "questions"

    id = db.Column(
        db.Integer,
        primary_key = True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable = False
    )

    content = db.Column(
        db.Text,
        nullable = False
    )

    created_at = db.Column(
        db.DateTime,
        default = db.func.current_timestamp(),
        nullable = False
    )

    def __init__(self, user_id, content, created_at = None):
        self.user_id = user_id
        self.content = content
        self.created_at = created_at if created_at else datetime.now()




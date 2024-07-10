from src import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key= True
        )

    username = db.Column(
        db.String(),
        nullable=False
        )

    location = db.Column(
        db.String()
        )

    def __init__(self, username, location):
        self.username = username
        self.location = location








from src import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key= True
    )

    username = db.Column(
        db.String(),
        nullable=False,
        unique=True
    )

    location = db.Column(
        db.String()
    )

    password = db.Column(
        db.String(100),
        nullable=False
    )

    def __init__(self, username, password, location):
        self.username = username
        self.password = password
        self.location = location





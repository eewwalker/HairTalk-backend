from src import db
from sqlalchemy.exc import IntegrityError
from .models import User

def create_user(name, location):
    try:
        user = User(name=name, location=location)
        db.session.add(user)
        db.session.commit()
        return user
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error creating user: {e}")


def read_user(id):
    try:
        return User.query.filter(User.id == id).first()
    except Exception as e:
        raise ValueError(f"Error reading user {id}: {e}")

def read_users():
    try:
        return User.query.all()
    except Exception as e:
        raise ValueError(f"Error reading users: {e}")

def update_user(id, name=None, location=None):
    try:
        user = User.query.filter(User.id == id).first()
        if user:
            if name:
                user.name = name
            if location:
                user.location = location
            db.session.commit()
            return user
        else:
            raise ValueError(f"Error updating user {id}")
    except Exception as e:
        db.session.rollback()
        raise ValueError(f"Error updating user {id}: {e}")


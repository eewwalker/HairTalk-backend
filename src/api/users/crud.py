from src import db
from sqlalchemy.exc import IntegrityError
from .models import User

def read_users():
    try:
        return User.query.all()
    except Exception as e:
        raise ValueError(f"Error reading users: {e}")

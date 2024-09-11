import click
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.users.models import User
from src.api.questions.models import Question, Answer, Comment
from datetime import datetime
import random
from flask_bcrypt import Bcrypt

#create Flask app
app = create_app()
cli = FlaskGroup(create_app=lambda: app)
bcrypt = Bcrypt(app)


@cli.command('recreate_db')
def recreate_db():
    """Drops and recreates the database."""
    db.drop_all()
    db.create_all()
    db.session.commit()
    click.echo("Database recreated!")


@cli.command('seed_users_questions_and_replies')
def seed_users_questions_and_replies():
    """Seeds the database with Users, Questions, and Replies."""

    user1 = User(
        username="sarahdarah",
        password=bcrypt.generate_password_hash('password').decode('utf-8'),
        location="San Francisco, California"
        )
    user2 = User(
        username="susanlucci",
        password=bcrypt.generate_password_hash('password').decode('utf-8'),
        location="Oakland, California"
        )
    user3 = User(
        username="sebastiancreastion",
        password=bcrypt.generate_password_hash('password').decode('utf-8'),
        location="Brooklyn, New York"
        )
    user4 = User(
        username="emilyengles",
        password=bcrypt.generate_password_hash('password').decode('utf-8'),
        location="Queens, New York"
        )
    db.session.add_all([user1, user2, user3, user4])
    db.session.commit()

    click.echo('added users')

    questions = [
        Question(
            user_id=user1.id,
            content='How to cut tight curls?',
            created_at=datetime(2024, 6, 24, 4, 0)
        ),
        Question(
            user_id=user1.id,
            content='What are non toxic color brands?',
            created_at=datetime(2024, 6, 24, 4, 0)
        ),
        Question(
            user_id=user2.id,
            content='Tip or No tip?',
            created_at=datetime(2024, 6, 24, 4, 0)
        ),
        Question(
            user_id=user1.id,
            content='How do you approach a color correction from all over level 10 to level 5?',
            created_at=datetime(2024, 6, 24, 4, 0)
        ),
    ]

    db.session.add_all(questions)
    db.session.commit()
    click.echo('added questions')

    answers = []
    for question in questions:
        for i in range(random.randint(1, 3)):
            answer = Answer(
                user_id=random.choice(
                    [user1.id, user2.id, user3.id, user4.id]),
                question_id=question.id,
                content=f'Answer {i + 1} for question {question.id}',
                created_at=datetime(2024, 6, 24, 5, 0 + i)
            )
            answers.append(answer)

    db.session.add_all(answers)
    db.session.commit()
    click.echo('added answers')

    comments = []
    for answer in answers:
        for j in range(random.randint(0, 3)):
            comment = Comment(
                user_id=random.choice(
                    [user1.id, user2.id, user3.id, user4.id]),
                answer_id=answer.id,
                content=f'Comment {j + 1} for answer {answer.id}',
                created_at=datetime(2024, 6, 24, 7, 0 + j)
            )
            comments.append(comment)

    db.session.add_all(comments)
    db.session.commit()
    click.echo('added comments')


if __name__ == "__main__":
    cli()
    app.run(threaded=True)

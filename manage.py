import click
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.users.models import User
from src.api.questions.models import Question
from datetime import datetime

app = create_app()
cli = FlaskGroup(create_app=lambda: app)

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


    user1 = User(name="Sarah Darah", location="SF")
    user2 = User(name="Susan Lucci", location="Oakland")
    db.session.add_all([user1, user2])
    db.session.commit()

    click.echo('added users')

    questions = [
        Question(
            user_id= user1.id,
            content = 'How to cut tight curls?',
            created_at= datetime(2024,6,24,4,0)
            ),
        Question(
            user_id= user1.id,
            content = 'What are non toxic color brands?',
            created_at= datetime(2024,6,24,4,0)
            ),
        Question(
            user_id= user2.id,
            content = 'Tip or No tip?',
            created_at= datetime(2024,6,24,4,0)
            ),
        Question(
            user_id= user1.id,
            content = 'How do you approach a color correction from all over level 10 to level 5?',
            created_at= datetime(2024,6,24,4,0)
            ),
    ]

    db.session.add_all(questions)
    db.session.commit()
    click.echo('added questions')

    # students = [
    #     User(name="Charlie Brown", phone_number="111-111-1111", role="student"),
    #     User(name="Lucy van Pelt", phone_number="222-222-2222", role="student"),
    #     User(name="Linus van Pelt", phone_number="333-333-3333", role="student"),
    #     User(name="Sally Brown", phone_number="444-444-4444", role="student")
    # ]
    #db.session.add_all(coaches + students )
    # db.session.commit()

    # start_date = datetime(2024, 5, 1)
    # end_date = datetime(2024, 8, 31)
    # delta_days = (end_date - start_date).days

    # appointments = []
    # reviews = []

    # for coach in coaches:
    #     for student in students:
    #         for _ in range(2):
    #             days_offset = random.randint(0, delta_days)
    #             appointment_date = start_date + timedelta(days=days_offset)
    #             appointment_time = datetime.combine(appointment_date, datetime.min.time()) + timedelta(hours=random.randint(9, 17))
    #             appointment = Appointment(coach_id=coach.id, start_time=appointment_time, student_id=random.choice([student.id, None]))
    #             appointments.append(appointment)

    # db.session.add_all(appointments)
    # db.session.commit()
    # db.session.add_all(reviews)
    # db.session.commit()

    # click.echo("Database seeded with initial users, comments, and replies.")

if __name__ == "__main__":
    cli()
    app.run(threaded=True)

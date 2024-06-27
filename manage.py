import click
from flask.cli import FlaskGroup
from src import create_app, db
from src.api.users.models import User

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
    """Seeds the database with Users, Appointments, and AppointmentReviews."""
    
    user = User(name="Sarah Darah", location="SF")
    db.session.add(user)
    db.session.commit()

    click.echo('added a user')
    # coaches = [
    #     User(name="Immanuel Kant", phone_number="123-456-7890", role="coach"),
    #     User(name="Thomas Hobbes", phone_number="098-765-4321", role="coach"),
    #     User(name="Lao Tzu", phone_number="555-555-5555", role="coach"),
    #     User(name="Hannah Arendt", phone_number="444-444-4444", role="coach")
    # ]
    
    # students = [
    #     User(name="Charlie Brown", phone_number="111-111-1111", role="student"),
    #     User(name="Lucy van Pelt", phone_number="222-222-2222", role="student"),
    #     User(name="Linus van Pelt", phone_number="333-333-3333", role="student"),
    #     User(name="Sally Brown", phone_number="444-444-4444", role="student")
    # ]
    
    # db.session.add_all(coaches + students)
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

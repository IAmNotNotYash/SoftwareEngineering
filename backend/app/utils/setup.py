from app import db
from app.models.user import User
from werkzeug.security import generate_password_hash
import sqlalchemy

def setup_default_admin(app):
    with app.app_context():
        try:
            # Using string 'admin' as the "email" (login identifier)
            admin = db.session.query(User).filter_by(email='admin@gmail.com').first()
            if not admin:
                admin = User(
                    email='admin@gmail.com',
                    password_hash=generate_password_hash('admin_pass'),
                    role='admin'
                )
                db.session.add(admin)
                db.session.commit()
                print("Default admin created automatically.")
        except (sqlalchemy.exc.ProgrammingError, sqlalchemy.exc.OperationalError):
            # Tables are not created yet. Rollback and skip.
            db.session.rollback()

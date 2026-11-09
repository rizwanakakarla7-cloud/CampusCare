
from flask_sqlalchemy import SQLAlchemy

# Create database object
db = SQLAlchemy()


def init_db(app):
    """Connect the application to the SQLite database."""

    db.init_app(app)

    with app.app_context():
        db.create_all()

    print("CampusCare database connected successfully!")

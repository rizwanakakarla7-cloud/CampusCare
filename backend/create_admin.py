
from getpass import getpass

from app import app
from database import db
from models import User
from werkzeug.security import generate_password_hash


with app.app_context():
    print("\n--- CampusCare Admin Account Setup ---")

    email = input("Enter admin email: ").strip().lower()
    password = getpass("Create admin password (minimum 8 characters): ")
    confirm_password = getpass("Confirm password: ")

    if not email or "@" not in email:
        print("Please enter a valid email.")
    elif len(password) < 8:
        print("Password must contain at least 8 characters.")
    elif password != confirm_password:
        print("Passwords do not match.")
    elif User.query.filter_by(email=email).first():
        print("This email is already registered. Use a different email.")
    else:
        admin = User(
            full_name="CampusCare Admin",
            email=email,
            password_hash=generate_password_hash(password),
            role="admin"
        )

        db.session.add(admin)
        db.session.commit()

        print("\nAdmin account created successfully!")
        print("You can now log in using this email and password.")

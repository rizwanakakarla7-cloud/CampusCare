
from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from database import db
from models import User

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# Student Registration
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    full_name = data.get("full_name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    student_id = data.get("student_id", "").strip()
    department = data.get("department", "").strip()

    if not full_name or not email or not password:
        return jsonify({
            "success": False,
            "message": "Name, email and password are required"
        }), 400

    if len(password) < 8:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 8 characters"
        }), 400

    if User.query.filter_by(email=email).first():
        return jsonify({
            "success": False,
            "message": "Email already registered"
        }), 409

    if student_id and User.query.filter_by(student_id=student_id).first():
        return jsonify({
            "success": False,
            "message": "Student ID already registered"
        }), 409

    user = User(
        full_name=full_name,
        email=email,
        student_id=student_id or None,
        department=department or None,
        password_hash=generate_password_hash(password),
        role="student"
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration successful"
    }), 201


# Login for Student and Admin
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({
            "success": False,
            "message": "Invalid email or password"
        }), 401

    login_user(user)

    return jsonify({
        "success": True,
        "message": "Login successful",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": user.role
        }
    })


# Logout
@auth_bp.route("/logout", methods=["POST"])
def logout():
    if current_user.is_authenticated:
        logout_user()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })

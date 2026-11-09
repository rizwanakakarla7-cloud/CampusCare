
import os

from flask import Flask, request, jsonify
from flask_login import (
    LoginManager,
    login_required,
    current_user
)

from database import db, init_db
import models
from routes.auth import auth_bp


# Project folders
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, "database")
os.makedirs(DATABASE_DIR, exist_ok=True)

DATABASE_PATH = os.path.join(DATABASE_DIR, "campuscare.db")

FRONTEND_DIR = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend")
)


# Create Flask application
app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)


# Application configuration
app.config["SECRET_KEY"] = os.environ.get(
    "SECRET_KEY",
    "campuscare-development-key"
)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///" + DATABASE_PATH.replace("\\", "/")
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Initialize database
init_db(app)


# Flask Login configuration
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(models.User, int(user_id))


# Register authentication routes
app.register_blueprint(auth_bp)


# Home page
@app.route("/")
def home():
    return app.send_static_file("index.html")


# Health check
@app.route("/health")
def health():
    return jsonify({
        "status": "success",
        "message": "CampusCare backend is running"
    })


# Student: Submit complaint
@app.route("/api/complaints", methods=["POST"])
@login_required
def submit_complaint():

    data = request.get_json(silent=True) or {}

    title = data.get("title", "").strip()
    category = data.get("category", "").strip()
    description = data.get("description", "").strip()
    location = data.get("location", "").strip()

    if not title or not category or not description:
        return jsonify({
            "success": False,
            "message": "Please fill all required fields"
        }), 400

    complaint = models.Complaint(
        title=title,
        category=category,
        description=description,
        location=location or None,
        user_id=current_user.id
    )

    db.session.add(complaint)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Complaint submitted successfully!",
        "complaint_id": complaint.id
    }), 201


# Student: View own complaints
@app.route("/api/complaints", methods=["GET"])
@login_required
def get_my_complaints():

    complaints = models.Complaint.query.filter_by(
        user_id=current_user.id
    ).order_by(
        models.Complaint.created_at.desc()
    ).all()

    return jsonify({
        "success": True,
        "complaints": [
            {
                "id": c.id,
                "title": c.title,
                "category": c.category,
                "description": c.description,
                "location": c.location,
                "status": c.status,
                "admin_remark": c.admin_remark
            }
            for c in complaints
        ]
    })


# Admin: View all complaints
@app.route("/api/admin/complaints", methods=["GET"])
@login_required
def admin_get_complaints():

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    complaints = models.Complaint.query.order_by(
        models.Complaint.created_at.desc()
    ).all()

    total = len(complaints)
    pending = sum(c.status == "Pending" for c in complaints)
    progress = sum(c.status == "In Progress" for c in complaints)
    resolved = sum(c.status == "Resolved" for c in complaints)

    return jsonify({
        "success": True,
        "counts": {
            "total": total,
            "pending": pending,
            "progress": progress,
            "resolved": resolved
        },
        "complaints": [
            {
                "id": c.id,
                "student_name": c.student.full_name,
                "category": c.category,
                "title": c.title,
                "description": c.description,
                "location": c.location,
                "status": c.status,
                "admin_remark": c.admin_remark
            }
            for c in complaints
        ]
    })


# Admin: Update complaint status
@app.route("/api/admin/complaints/<int:complaint_id>", methods=["PATCH"])
@login_required
def admin_update_complaint(complaint_id):

    if current_user.role != "admin":
        return jsonify({
            "success": False,
            "message": "Admin access required"
        }), 403

    data = request.get_json(silent=True) or {}

    new_status = data.get("status", "").strip()
    remark = data.get("admin_remark", "").strip()

    allowed_statuses = [
        "Pending",
        "In Progress",
        "Resolved"
    ]

    if new_status not in allowed_statuses:
        return jsonify({
            "success": False,
            "message": "Invalid complaint status"
        }), 400

    complaint = db.session.get(
        models.Complaint,
        complaint_id
    )

    if not complaint:
        return jsonify({
            "success": False,
            "message": "Complaint not found"
        }), 404

    complaint.status = new_status
    complaint.admin_remark = remark

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Complaint updated successfully"
    })


# Run application
if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5001,
        debug=False,
        use_reloader=False
    )

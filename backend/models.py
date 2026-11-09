
from datetime import datetime, timezone

from database import db
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """Stores student and admin account details."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    full_name = db.Column(
        db.String(100),
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False,
        index=True
    )

    student_id = db.Column(
        db.String(30),
        unique=True,
        nullable=True
    )

    department = db.Column(
        db.String(100),
        nullable=True
    )

    password_hash = db.Column(
        db.String(255),
        nullable=False
    )

    role = db.Column(
        db.String(20),
        nullable=False,
        default="student"
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    complaints = db.relationship(
        "Complaint",
        back_populates="student",
        cascade="all, delete-orphan"
    )


class Complaint(db.Model):
    """Stores campus complaint information."""

    __tablename__ = "complaints"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    title = db.Column(
        db.String(150),
        nullable=False
    )

    category = db.Column(
        db.String(50),
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    location = db.Column(
        db.String(150),
        nullable=True
    )

    status = db.Column(
        db.String(30),
        nullable=False,
        default="Pending"
    )

    admin_remark = db.Column(
        db.Text,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    updated_at = db.Column(
        db.DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc)
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    student = db.relationship(
        "User",
        back_populates="complaints"
    )

from datetime import datetime
from .db import db
from models.db import db


class User(db.Model):
    __tablename__ = 'user'  # ✅ Important: must match what Password model expects

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    passwords = db.relationship('Password', backref='user', lazy=True)

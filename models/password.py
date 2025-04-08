from datetime import datetime
from .db import db

class Password(db.Model):
    __tablename__ = 'password'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    password_name = db.Column(db.String(100), nullable=False)
    generated_password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('user_id', 'password_name', name='unique_user_password_name'),
    )

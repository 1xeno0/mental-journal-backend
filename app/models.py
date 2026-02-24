import uuid
from datetime import datetime
from sqlalchemy.dialects.postgresql import UUID
from .extensions import db

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    entries = db.relationship('Entry', backref='author', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    tags = db.Column(db.JSON, nullable=True)
    note = db.Column(db.Text, nullable=False)
    ai_response = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'mood': self.mood,
            'tags': self.tags,
            'note': self.note,
            'ai_response': self.ai_response,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

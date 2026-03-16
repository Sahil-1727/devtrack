from app import db
from flask_login import UserMixin
from datetime import datetime
import secrets

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    api_token = db.Column(db.String(64), unique=False, nullable=True)

    applications = db.relationship('Application', backref='applicant', lazy=True)

    def generate_token(self):
        self.api_token = secrets.token_hex(32)
        return self.api_token

    def __repr__(self):
        return f'<User {self.username}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Applied')
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Application {self.company} - {self.role}>'
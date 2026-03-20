from app import db
from flask_login import UserMixin
from datetime import datetime
import secrets

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    api_token = db.Column(db.String(64), nullable=True)

    # Academic profile — ML model will use these
    cgpa = db.Column(db.Float, nullable=True)
    backlogs = db.Column(db.Integer, default=0)
    college = db.Column(db.String(100), nullable=True)
    graduation_year = db.Column(db.Integer, nullable=True)
    branch = db.Column(db.String(50), nullable=True)

    # Experience profile
    internship_count = db.Column(db.Integer, default=0)
    project_count = db.Column(db.Integer, default=0)
    skills = db.Column(db.Text, nullable=True)

    # Relationships
    applications = db.relationship('Application', backref='applicant', lazy=True)

    def generate_token(self):
        self.api_token = secrets.token_hex(32)
        return self.api_token

    def skills_list(self):
        if self.skills:
            return [s.strip() for s in self.skills.split(',')]
        return []

    def __repr__(self):
        return f'<User {self.username}>'


class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='Applied')
    date_applied = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.Text, nullable=True)

    # New fields for better tracking + ML data
    location = db.Column(db.String(100), nullable=True)
    job_type = db.Column(db.String(20), nullable=True, default='Internship')
    salary = db.Column(db.Integer, nullable=True)
    source = db.Column(db.String(50), nullable=True)
    interview_date = db.Column(db.DateTime, nullable=True)
    response_days = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Application {self.company} - {self.role}>'
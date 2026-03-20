from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional, NumberRange
from app.models import User
from flask_login import current_user

class ApplicationForm(FlaskForm):
    company = StringField('Company Name', validators=[
        DataRequired(),
        Length(max=100)
    ])
    role = StringField('Role / Position', validators=[
        DataRequired(),
        Length(max=100)
    ])
    status = SelectField('Status', choices=[
        ('Applied', 'Applied'),
        ('Interview', 'Interview'),
        ('Offer', 'Offer'),
        ('Rejected', 'Rejected')
    ])
    location = StringField('Location', validators=[Optional(), Length(max=100)])
    job_type = SelectField('Job Type', choices=[
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time')
    ])
    salary = IntegerField('Salary / Stipend (monthly)', validators=[Optional()])
    source = SelectField('Found on', choices=[
        ('LinkedIn', 'LinkedIn'),
        ('Internshala', 'Internshala'),
        ('Unstop', 'Unstop'),
        ('Company Website', 'Company Website'),
        ('Referral', 'Referral'),
        ('Other', 'Other')
    ])
    notes = TextAreaField('Notes', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Save Application')


class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
    college = StringField('College', validators=[Optional(), Length(max=100)])
    branch = StringField('Branch', validators=[Optional(), Length(max=50)])
    graduation_year = IntegerField('Graduation Year', validators=[Optional()])
    cgpa = FloatField('CGPA (out of 10)', validators=[
        Optional(),
        NumberRange(min=0, max=10, message='CGPA must be between 0 and 10')
    ])
    backlogs = IntegerField('Number of Backlogs', validators=[
        Optional(),
        NumberRange(min=0, message='Cannot be negative')
    ])
    internship_count = IntegerField('Internships Done', validators=[Optional()])
    project_count = IntegerField('Projects Built', validators=[Optional()])
    skills = StringField('Skills (comma separated)', validators=[Optional(), Length(max=500)])
    submit = SubmitField('Update Profile')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username already taken.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already registered.')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[
        DataRequired(),
        Length(min=6)
    ])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password')
    ])
    submit = SubmitField('Change Password')
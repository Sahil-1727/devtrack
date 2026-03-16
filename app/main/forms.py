from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, Optional
from app.models import User
from flask_login import current_user

from app.models import User

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
    notes = TextAreaField('Notes', validators=[
        Length(max=500)
    ])
    submit = SubmitField('Add Application')

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20)
    ])
    email = StringField('Email', validators=[
        DataRequired(),
        Email()
    ])
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
    current_password = StringField('Current Password',validators=[
        DataRequired(),
        Length(min=6, max=20)
    ])

    new_password = StringField('New_Password',validators=[
        DataRequired(),
        Length(min=6, max=20)
    ])

    confirm_password = StringField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password')
    ])
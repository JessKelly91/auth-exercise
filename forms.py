from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Email, EqualTo, Length

class RegistrationForm(FlaskForm):
    """Create registration form"""

    username = StringField("Username", 
                           validators=[
                               InputRequired(), 
                               Length(min=1, max=20, message="Username must be between 1 and 20 characters.")])
    password = PasswordField("Password", 
                             validators=[
                                 InputRequired(), 
                                 EqualTo('confirm', message='Passwords must match.')])
    confirm = PasswordField("Confirm Password", 
                            validators=[InputRequired()])
    email = EmailField("Email", 
                       validators=[
                           InputRequired(), 
                           Email(), 
                           Length(min=1, max=50, message="Email must be between 1 and 50 characters.")])
    first_name = StringField("First Name", 
                             validators=[
                                 InputRequired(), 
                                 Length(min=1, max=30, message="First name must be between 1 and 30 characters.")])
    last_name = StringField("Last Name", 
                            validators=[
                                InputRequired(), 
                                Length(min=1, max=30, message="Last name must be between 1 and 30 characters.")])

class LoginForm(FlaskForm):
    """Login Form"""

    username = StringField("Username", 
                           validators=[
                               InputRequired(), 
                               Length(min=1, max=20, message="Username must be between 1 and 20 characters.")])
    password = PasswordField("Password", 
                             validators=[InputRequired()])

class FeedbackForm(FlaskForm):
    """Feedback form"""
    title = StringField("Title",
                        validators=[
                            InputRequired(), 
                            Length(min=1, max=100)])
    content = TextAreaField("Content", 
                            validators=[InputRequired()])
    
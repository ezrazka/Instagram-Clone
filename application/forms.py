from flask_wtf import FlaskForm
flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application import db

class LoginForm(FlaskForm):
    pass

class SignUpForm(FlaskForm):
    pass

class EditProfile(FlaskForm):
    pass

class CreatePost(FlaskForm):
    pass

class EditPost(FlaskForm):
    pass
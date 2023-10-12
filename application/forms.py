from flask_wtf import FlaskForm
flask_wtf.file import FileField
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application import db

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Login")

class CreateNoteForm(FlaskForm):
    note = StringField("Note", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Add Note")

class UpdateNoteForm(FlaskForm):
    note = StringField("Note", validators=[DataRequired(), Length(min=5)])
    submit = SubmitField("Update Note")
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Login")

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match")])
    submit = SubmitField("Sign Up")

class EditProfile(FlaskForm):
    fullname = StringField("Full Name", validators=[Length(min=4, max=8)])
    profile_pic = StringField("Profile Picture", validators=[Length(max=255)])
    bio = StringField("Full Name", validators=[Length(max=255)])
    submit = SubmitField("Save Changes")

class CreatePost(FlaskForm):
    post_image = StringField("Post", validators=[DataRequired(), Length(min=5)])
    post_caption = StringField("Caption", validators=[Length(max=1023)])
    submit = SubmitField("Add Post")

class EditPost(FlaskForm):
    post_caption = StringField("Caption", validators=[Length(max=1023)])
    submit = SubmitField("Save Changes")
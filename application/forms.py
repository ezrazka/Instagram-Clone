from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exists_email, exists_username, not_exists_username

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), not_exists_username], render_kw={"placeholder": "Enter your username"})
    password = PasswordField("password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("login")

class SignUpForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=12), exists_username], render_kw={"placeholder": "Enter your username"})
    fullname = StringField("full name", validators=[Length(min=4, max=16)], render_kw={"placeholder": "Enter your full name"})
    email = EmailField("email", validators=[DataRequired(), Email(), exists_email], render_kw={"placeholder": "Enter a valid email address"})
    password = PasswordField("password", validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("confirm password", validators=[DataRequired(), EqualTo("password", message="Password must match")], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("sign up")

class EditProfileForm(SignUpForm):
    username = StringField("username", validators=[DataRequired(), Length(min=4, max=12)])
    password = None
    confirm_password = None
    email = None
    bio = StringField("bio")
    profile_pic = FileField("profile picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("update profile")

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField("old password", validators=[DataRequired(), Length(min=8)])
    new_password = PasswordField("new password", validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField("confirm new password", validators=[DataRequired(), Length(min=8), EqualTo("new_password", message="Password must match")])
    submit = SubmitField("reset password")

class VerificationResetPasswordForm(FlaskForm):
    new_password = PasswordField("new password", validators=[DataRequired(), Length(min=8)])
    confirm_new_password = PasswordField("confirm new password", validators=[DataRequired(), Length(min=8), EqualTo("new_password", message="Password must match")])
    submit = SubmitField("reset password")

class ForgotPasswordForm(FlaskForm):
    email = PasswordField("email", validators=[DataRequired(), not_exists_email])
    # recaptcha = RecaptchaField()
    submit = SubmitField("send link verification to email")

class CreatePostForm(FlaskForm):
    post_pic = FileField("picture", validators=[DataRequired(), FileAllowed(["jpg", "jpeg", "png"])])
    caption = TextAreaField("caption")
    submit = SubmitField("post")

class EditPostForm(FlaskForm):
    caption = StringField("caption")
    submit = SubmitField("update post")
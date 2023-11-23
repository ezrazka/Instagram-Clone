from flask_wtf import FlaskForm, RecaptchaField
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField, EmailField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo

from application.utils import exists_email, not_exists_email, exists_username, not_exists_username

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), not_exists_username], render_kw={"placeholder": "Enter your username"})
    password = PasswordField("Password", validators=[DataRequired()], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

class SignUpForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=12), exists_username], render_kw={"placeholder": "Enter your username"})
    fullname = StringField("Full Name", validators=[Length(min=4, max=16)], render_kw={"placeholder": "Enter your full name"})
    email = EmailField("Email", validators=[DataRequired(), Email(), exists_email], render_kw={"placeholder": "Enter a valid email address"})
    password = PasswordField("Password", validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField("Confirm Password", validators=[DataRequired(), EqualTo("password", message="Password must match")], render_kw={"placeholder": "Confirm password"})
    submit = SubmitField("Sign Up")

class EditProfileForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=4, max=12)], render_kw={"placeholder": "Enter your username"})
    fullname = StringField("Full Name", validators=[Length(min=4, max=16)], render_kw={"placeholder": "Enter your full name"})
    bio = TextAreaField("Bio", render_kw={"placeholder": "Enter your bio"})
    profile_pic = FileField("Profile Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Update Profile")

class ResetPasswordForm(FlaskForm):
    old_password = PasswordField("Old Password", validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "Old password"})
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "New password"})
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=8), EqualTo("new_password", message="Password must match")], render_kw={"placeholder": "Confirm new password"})
    submit = SubmitField("Reset Password")

class VerificationResetPasswordForm(FlaskForm):
    new_password = PasswordField("New Password", validators=[DataRequired(), Length(min=8)], render_kw={"placeholder": "New password"})
    confirm_new_password = PasswordField("Confirm New Password", validators=[DataRequired(), Length(min=8), EqualTo("new_password", message="Password must match")], render_kw={"placeholder": "Confirm new password"})
    submit = SubmitField("Reset Password")

class ForgotPasswordForm(FlaskForm):
    email = PasswordField("Email", validators=[DataRequired(), not_exists_email], render_kw={"placeholder": "Enter a valid email address"})
    # recaptcha = RecaptchaField()
    submit = SubmitField("Send Verification Link to Email")

class CreatePostForm(FlaskForm):
    post_pic = FileField("Post Picture", validators=[DataRequired(), FileAllowed(["jpg", "jpeg", "png"])])
    caption = TextAreaField("Caption", render_kw={"placeholder": "Write a caption"})
    submit = SubmitField("Post")

class EditPostForm(FlaskForm):
    caption = StringField("Caption", render_kw={"placeholder": "Write a caption"})
    submit = SubmitField("Update Post")
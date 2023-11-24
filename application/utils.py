import os
import secrets
from PIL import Image
from datetime import datetime, timedelta

from flask import current_app

from wtforms.validators import ValidationError

from application import login_manager
from application.models import User

# FORM UTILS
def exists_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if user:
        raise ValidationError(
            "Email already exists. Please use a different email.")


def not_exists_email(form, email):
    user = User.query.filter_by(email=email.data).first()
    if not user:
        raise ValidationError("Email not found.")


def exists_username(form, username):
    user = User.query.filter_by(username=username.data).first()
    if user:
        raise ValidationError(
            "Username already exists. Please use a different username.")
# END OF FORM UTILS

# LOGIN MANAGER UTILS
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
# END OF LOGIN MANAGER UTILS

# IMAGE SAVE UTILS
def save_image(form_picture_data, folder_name):
    random_hex = secrets.token_hex(5)
    while any(file.startswith(random_hex) for file in f'images/{folder_name}/'):
        random_hex = secrets.token_hex(5)
    _, f_ext = os.path.splitext(form_picture_data.filename)
    file_name = random_hex + f_ext
    picture_fn = f'images/{folder_name}/' + file_name
    picture_path = os.path.join(current_app.root_path, 'static/', picture_fn)

    image = Image.open(form_picture_data)
    image.save(picture_path)

    return file_name
# END OF IMAGE SAVE UTILS

# PARSER UTILS
def parseDate(date):
    current_date = datetime.utcnow()

    if current_date - date < timedelta(minutes=1):
        seconds_diff = int((current_date - date).total_seconds())
        return f'{seconds_diff} second{"s" if seconds_diff > 1 else ""} ago'
    if current_date - date < timedelta(hours=1):
        minutes_diff = int((current_date - date).total_seconds() / 60)
        return f'{minutes_diff} minute{"s" if minutes_diff > 1 else ""} ago'
    if current_date - date < timedelta(days=1):
        hours_diff = int((current_date - date).total_seconds() / (60 * 60))
        return f'{hours_diff} hour{"s" if hours_diff > 1 else ""} ago'
    if current_date - date < timedelta(days=7):
        days_diff = int((current_date - date).total_seconds() / (60 * 60 * 24))
        return f'{days_diff} day{"s" if days_diff > 1 else ""} ago'
    if current_date - date < timedelta(days=8):
        return '1 week ago'
    
    if current_date.year == date.year:
        return f'{date.strftime("%B")} {date.day}'
    return f'{date.strftime("%B")} {date.day}, {date.year}'
# END OF PARSER UTILS
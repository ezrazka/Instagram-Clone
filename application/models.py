from application import db
from datetime import datetime

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    active = db.Column(db.Boolean, nullable=False)
    username = db.Column(db.String(31), nullable=False)
    profile_photo_url = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
                         
class Relationship(db.Model):
    __tablename__ = "relationships"
    id = db.Column(db.Integer, primary_key=True)
    follower = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    following = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    status = db.Column(db.Boolean, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Post(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    caption = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    content = db.Column(db.String(1023), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

class Like(db.Model):
    __tablename__ = "likes"
    id = db.Column(db.Integer, primary_key=True)
    post = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
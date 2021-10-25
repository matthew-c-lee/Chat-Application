from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

# class Message(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     from_user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one-to-many relationship
#     to_user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one-to-many relationship


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one-to-many relationship

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    answer = db.Column(db.String(150)) # security word
    question = db.Column(db.String(150)) # security question
    first_name = db.Column(db.String(150))
    selected_friend_id = db.Column(db.Integer)
    messages = db.relationship('Message')
    # messages = db.relationship('Message')
# file stores database models

from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import pytz


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now(tz=pytz.timezone('US/Eastern')))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one-to-many relationship
    recipient_id = db.Column(db.Integer)
    group_id = db.Column(db.Integer)



class Friend(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one-to-many relationship
    friend_id = db.Column(db.Integer)
    friend_name = db.Column(db.String(10000))

user_groups = db.Table('user_groups',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('group_id', db.Integer, db.ForeignKey('group.group_id'))
)
class Block(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #one-to-many relationship
    blocked_id = db.Column(db.Integer)
    blocked_name = db.Column(db.String(10000))
    
class User(db.Model, UserMixin):
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    answer = db.Column(db.String(150)) # security word
    question = db.Column(db.String(150)) # security question
    text_color = db.Column(db.String(20), default='Black') # message text color
    text_size = db.Column(db.String(20), default='Medium') # message text size
    background = db.Column(db.String(20), default='White') # background color
    status = db.Column(db.String(150))
    messages = db.relationship('Message')
    friends_list = db.relationship('Friend')
    block_list = db.relationship('Block')

    id = db.Column(db.Integer, primary_key=True)
    groups = db.relationship('Group', secondary=user_groups, backref=db.backref('members', lazy='dynamic'))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20))



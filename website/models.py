from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
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
 
class User(db.Model, UserMixin):
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    answer = db.Column(db.String(150)) # security word
    question = db.Column(db.String(150)) # security question
    first_name = db.Column(db.String(150))
    status = db.Column(db.String(150))
    messages = db.relationship('Message')
    friends_list = db.relationship('Friend')

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    groups = db.relationship('Group', secondary=user_groups, backref=db.backref('members', lazy='dynamic'))

class Group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(20))
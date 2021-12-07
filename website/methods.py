import secrets
import os
import datetime
from PIL import Image

from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user

from sqlalchemy import and_, desc, or_

from .models import User, Message, Friend, Block, Request
from . import db
from .forms import UpdateAccountForm, SettingsForm

# METHOD
# Deletes message
def delete_message(message_id):
    message = Message.query.get(message_id)

    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

# METHOD
# Searches for the corresponding Block record in the Block table and remove it.
def remove_block(user_id):
    user = User.query.get(user_id)

    # Find the Block record that needs to be removed
    block_record = Block.query.filter(Block.user_id == current_user.id, Block.blocked_id==user.id, Block.blocked_name==user.username).first()
    db.session.delete(block_record)
    db.session.commit()
    flash("You have unblocked " + user.username, category='success')

# METHOD
# After checking if the user exists, The selected user will be sent a Friend Request by adding the request's
# information to the Request table.
def send_friend_request(user_id):
    user = User.query.get(user_id)
    
    if user:
        new_request = Request(user_id = current_user.id, receiver_id = user.id, receiver_name = user.username)
        db.session.add(new_request)
        db.session.commit()
        
        flash("You have sent a friend request to " + user.username, category = 'success')

def delete_friend(user_id):
    user = User.query.get(user_id)

    # Find friend record where the User ID is the CURRENT user's, and the Friend ID is the friend's
    your_friend_record = Friend.query.filter(Friend.user_id == current_user.id, Friend.friend_id == user.id).first()

    # Find friend record where the User ID is the friend's, and the Friend ID is the CURRENT user's
    their_friend_record = Friend.query.filter(Friend.user_id == user_id, Friend.friend_id == current_user.id).first()

    if your_friend_record:
        db.session.delete(your_friend_record)
        db.session.delete(their_friend_record)
        db.session.commit()


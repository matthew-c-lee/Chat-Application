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
from .methods import *

routes = Blueprint('routes', __name__)

# saves the picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(routes.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

# This loads the CURRENT user's profile page using a form from the forms.py file. Using this, we validate
# the form data to ensure no disallowed inputs are submitted. This page also includes the CURRENT user's 
# incoming Friend Requests and Block List, both of which they can interact with.
@routes.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    # If the form has been submitted with valid data:
    if form.validate_on_submit():
        # If the user uploaded an image
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            # Update the user's image
            current_user.image_file = picture_file
        
        # Update the user's username and status
        current_user.username = form.username.data
        current_user.status = form.status.data
        db.session.commit()   #update database
   
        # Tell the user
        flash('Your account has been updated!', 'success')
        return redirect('/profile')

    # if you have loaded the page
    elif request.method == 'GET':
        # fills out the forms based on your current username and status
        form.username.data = current_user.username
        form.status.data = current_user.status

    # grabs the image out of the profile pics folder
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('profile.html', title = 'Account', image_file = image_file, form = form, 
        user = current_user, User = User, Request = Request)


# This loads the profile page for OTHER users. This shows the selected user's username, status, profile
# picture, and the interactions you can have with the user (block, friend, unfriend, unblock depending on
# their appearance in your lists or not. 
@routes.route('/profile/<string:username>', methods = ['GET', 'POST'])
@login_required
def other_profile(username):
    user = User.query.filter(User.username == username).first_or_404()  #get user data
    
    # Check that the user exists
    if user:
        # Grab their profile picture
        image_file = url_for('static', filename = 'profile_pics/' + user.image_file)  

        return render_template('other_profile.html', Friend = Friend, user = user, image_file = image_file, 
            current_user = current_user, and_ = and_ , Block = Block, Request = Request)


# This route will be activated upon the press of the 'Add Friend' button anywhere in the application. The button 
# is only accessible if the other user has sent the CURRENT user a friend request. The users will then be added 
# as mutual friends within the Friend table.
@routes.route('/add-friend/<string:user_id>', methods = ['GET', 'POST'])
@login_required
def add_friend(user_id):
    user = User.query.get(user_id)

    # if the user exists
    if user:
        # Friend record for the friend that requested you
        new_friend = Friend(user_id = current_user.id, friend_id = user.id, friend_name = user.username)
        # Friend record for the you
        user_friend = Friend(user_id = user.id, friend_id = current_user.id, friend_name = current_user.username)
        # The request to be deleted
        old_request = Request.query.filter(Request.user_id == user.id, Request.receiver_id==current_user.id).first()
        db.session.delete(old_request)
        db.session.add(new_friend)
        db.session.add(user_friend)
        db.session.commit()  # Update Database
        
        flash("You are now friends with " + user.username)
    return redirect('/profile')


# BUTTON CODE
# This route will be activated upon the press of the 'Send Request' button in the search bar. It will run
# the send_friend_request method, then redirect to search.
@routes.route('/request-friend/<string:user_id>/<string:search>', methods = ['GET', 'POST'])
@login_required
def request_friend(user_id, search):
    send_friend_request(user_id)
    return redirect("/search/" + search)


# BUTTON CODE
# This route will be activated upon the press of the 'Send Request' button anywhere on another user's 
# profile. It will run the send_friend_request method, then redirect to the chat.
@routes.route('/request-friend-profile/<string:user_id>', methods = ['GET', 'POST'])
@login_required
def request_friend_profile(user_id):
    send_friend_request(user_id)

    user = User.query.get(user_id)

    return redirect('/profile/' + user.username)

# BUTTON CODE
# Uses delete_message method
@routes.route('/delete-message/<string:message_id>/<string:recipient_name>', methods = ['GET', 'POST'])
def delete_message_route(message_id, recipient_name):
    delete_message(message_id)

    return redirect('/chat/' + recipient_name)


# BUTTON CODE
# This route is used for the Block button. If the two users are friends, it will mutually unfriend them. It will
# also add the user to your Block List.
@routes.route('/add-block/<string:user_id>', methods=['GET', 'POST'])
def add_block(user_id):
    user = User.query.get(user_id)
    delete_friend(user_id)

    # Block the user
    new_block = Block(user_id=current_user.id, blocked_id=user.id, blocked_name=user.username)
    db.session.add(new_block)
    db.session.commit()

    flash("You have blocked " + user.username, category='success')

    return redirect('/profile/' + user.username)


# BUTTON CODE
# This route is for the Unblock button accessed via YOUR profile
@routes.route('/remove-block-profile/<string:user_id>', methods=['GET', 'POST'])
def remove_block_profile(user_id):
    remove_block(user_id)    
    return redirect('/profile')


# BUTTON CODE
# This route is for the Unblock button accessed via the SELECTED USER'S profile 
@routes.route('/remove-block-their-profile/<string:user_id>', methods=['GET', 'POST'])
def remove_block_their_profile(user_id):
    remove_block(user_id)    

    user = User.query.get(user_id)
    return redirect('/profile/' + user.username)


# BUTTON CODE
# Deny any friend request
@routes.route('/deny-friend/<string:user_id>', methods = ['GET', 'POST'])
def deny_friend(user_id):

    user = User.query.get(user_id)
    request_record = Request.query.filter(Request.user_id == user.id, Request.receiver_id==current_user.id).first()
    db.session.delete(request_record)
    db.session.commit()
    
    flash("You have denied " + user.username, category = 'success')

    return redirect('/profile')


# BUTTON CODE
# This route is used for the Remove Friend button accessed via their profile. It runs delete_friend and
# redirects the user back to the selected profile.
@routes.route('/remove-friend/<string:user_id>', methods=['GET', 'POST'])
def remove_friend(user_id):
    delete_friend(user_id)
    
    user = User.query.get(user_id)
    flash("You have unfriended " + user.username, category='success')

    return redirect('/profile/' + user.username)


# This route brings up the basic search page before any queries are inputted. Upon a submission, this route will redirect
# the user to the other_search route.
@routes.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    user_db = None
    search = None
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)

    return render_template("search.html", user = current_user, current_user = current_user, user_db = user_db, 
        search = search, Friend = Friend, and_ = and_, Block = Block, Request = Request)


# This route is for user searches. It is accessible after the user has entered a query into the search bar.
# It will use wildcards to limit the database to only those users with the search in their name, and send those
# results to the user.
@routes.route('/search/<string:search>', methods = ['GET', 'POST'])
@login_required
def other_search(search):
    # uses wildcards to search for users with those characters
    search_list = User.query.filter(User.username.like('%'+search+'%')).all()  
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)


    return render_template("search.html", user = current_user, current_user = current_user, search_list = search_list, 
        search = search, Friend = Friend, and_ = and_, Block = Block, Request = Request)


# This route brings up the Settings Page. It will use a form from forms.py to autofill the forms with the user's
# current settings. The code checks for a valid submission and updates the user's settings accordingly.
@routes.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.text_color = form.text_color.data
        current_user.text_size = form.text_size.data
        current_user.background = form.background.data

        db.session.commit()

        flash('Your settings were changed.', category = 'success')
        return redirect('/settings')

    
    elif request.method == 'GET':
        # fills out the forms based on your current settings
        form.text_color.data = current_user.text_color
        form.text_size.data = current_user.text_size
        form.background.data = current_user.background

    return render_template("settings.html", User = User, user = current_user, username = current_user.username, form = form)


# This route brings up the Frequently Asked Questions page.
@routes.route('/faq', methods = ['GET', 'POST'])
def faq():
    return render_template("faq.html", user = current_user)


# This route brings up the Chat Menu. 
@routes.route('/', methods = ['GET', 'POST'])
@login_required
def chat():
    return render_template("chat_menu.html", User = User, user = current_user, username = current_user.username, 
        Message = Message, desc = desc, redirect = redirect, and_ = and_, or_ = or_, datetime = datetime)


# This route allows you to chat with a selected user. If a message is valid, it will
# add it to the Message table.
@routes.route('/chat/<string:recipient>', methods = ['GET', 'POST'])
@login_required
def chat_with(recipient):
    recipient = User.query.filter(User.username == recipient).first_or_404()

    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category = 'error')
        else:
            new_message = Message(data = message, user_id = current_user.id, recipient_id = recipient.id)
            db.session.add(new_message)
            db.session.commit()   #update database
            return redirect('/chat/' + recipient.username)
 
    return render_template("chat_with.html", User = User, user = current_user, username = current_user.username, 
        Message = Message, recipient = recipient, desc = desc, redirect = redirect, message1 = None, datetime = datetime)
    
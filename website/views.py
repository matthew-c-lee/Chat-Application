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

views = Blueprint('views', __name__)


# saves the picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(views.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# your profile page
@views.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        
        current_user.username = form.username.data
        current_user.status = form.status.data
        db.session.commit()   #update database

        flash('Your account has been updated!', 'success')
        return redirect(url_for('views.profile'))

    # if you have loaded the page
    elif request.method == 'GET':
        # fills out the forms based on your current username and status
        form.username.data = current_user.username
        form.status.data = current_user.status

    # grabs the image out of the profile pics folder
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('profile.html', title = 'Account', image_file = image_file, form = form, 
        user = current_user, User = User, Request = Request)


# profile of a specific user
@views.route('/profile/<string:username>', methods = ['GET', 'POST'])
@login_required
def other_profile(username):
    user = User.query.filter(User.username == username).first_or_404()  #get user data
    
    if user:
        image_file = url_for('static', filename = 'profile_pics/' + user.image_file)  

        if request.method == 'POST':
            user.username = request.form['username']

            try:
                db.session.commit()   #update database
                return redirect('/')
            except:
                return 'There was an issue updating your task'

        return render_template('other_profile.html', Friend = Friend, user = user, image_file = image_file, 
            current_user = current_user, and_ = and_ , Block = Block)


# Code for the Add Friend button
@views.route('/add-friend/<string:user_id>/<string:search>', methods = ['GET', 'POST'])
@login_required
def add_friend(user_id, search):
    user = User.query.get(user_id)

    # if the user exists
    if user:
        new_friend = Friend(user_id = current_user.id, friend_id = user.id, friend_name = user.username)
        db.session.add(new_friend)
        db.session.commit()
        
        flash("You are now friends with " + user.username, category = 'success')
    return redirect("/search/" + search)

@views.route('/request-friend/<string:user_id>/<string:search>', methods = ['GET', 'POST'])
@login_required
def request_friend(user_id, search):
    user = User.query.get(user_id)

    # if the user exists
    if user:
        new_request = Request(user_id = current_user.id, receiver_id = user.id, receiver_name = user.username)
        db.session.add(new_request)
        db.session.commit()
        
        flash("You have sent a friend request to " + user.username, category = 'success')
    return redirect("/search/" + search)

@views.route('/add-friend/<string:user_id>', methods = ['GET', 'POST'])
@login_required
def add_friend_profile(user_id):
    user = User.query.get(user_id)

    # if the user exists
    if user:
        new_friend = Friend(user_id = current_user.id, friend_id = user.id, friend_name = user.username)
        db.session.add(new_friend)
        db.session.commit()
        
        flash("You are now friends with " + user.username, category = 'success')
    return redirect('/')


# Deletes messages
@views.route('/delete-message/<string:message_id>/<string:recipient_name>', methods = ['GET', 'POST'])
def delete_message(message_id, recipient_name):
    message = Message.query.get(message_id)
    
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()   #update database

    return redirect('/chat/' + recipient_name)
    

@views.route('/add-block/<string:user_id>', methods=['GET', 'POST'])
def add_block(user_id):

    user = User.query.get(user_id)

    new_block = Block(user_id=current_user.id, blocked_id=user.id, blocked_name=user.username)
    old_friend = Friend.query.filter(Friend.user_id == current_user.id, Friend.friend_id==user.id, Friend.friend_name==user.username).first()
    db.session.add(new_block)
    db.session.commit()

    if old_friend:
        db.session.delete(old_friend)
        db.session.commit()


    flash("You have blocked " + user.username, category='success')

    return redirect(url_for('views.chat'))

# Code for unblock button
@views.route('/remove-block/<string:user_id>', methods = ['GET', 'POST'])
def remove_block(user_id):

    user = User.query.get(user_id)

    old_block = Block.query.filter(Block.user_id == current_user.id).first()
    db.session.delete(old_block)
    db.session.commit()
    
    flash("You have unblocked " + user.username, category = 'success')

    return redirect(url_for('views.chat'))

@views.route('/remove-friend/<string:user_id>', methods=['GET', 'POST'])
def remove_friend(user_id):

    user = User.query.get(user_id)

    #new_block = Block(user_id=current_user.id, blocked_id=user.id, blocked_name=user.username)
    old_friend = Friend.query.filter(Friend.user_id == current_user.id, Friend.friend_id==user.id, Friend.friend_name==user.username).first()
    db.session.delete(old_friend)
    db.session.commit()
    
    flash("You have unfriended " + user.username, category='success')

    return redirect(url_for('views.chat'))


# search before the user inputs a query
@views.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    user_db = None
    search = None
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)

    return render_template("search.html", user = current_user, current_user = current_user, user_db = user_db, 
        search = search, Friend = Friend, and_ = and_, Block = Block, Request = Request)


# search with query
@views.route('/search/<string:search>', methods = ['GET', 'POST'])
@login_required
def other_search(search):
    # uses wildcards to search for users with those characters
    user_db = User.query.filter(User.username.like('%'+search+'%')).all()  
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)


    return render_template("search.html", user = current_user, current_user = current_user, user_db = user_db, 
        search = search, Friend = Friend, and_ = and_, Block = Block, Request = Request)


# settings page
@views.route('/settings', methods = ['GET', 'POST'])
@login_required
def settings():
    form = SettingsForm()
    if form.validate_on_submit():
        current_user.text_color = form.text_color.data
        current_user.text_size = form.text_size.data
        current_user.background = form.background.data

        db.session.commit()

        flash('Your settings were changed.', category = 'success')
        return redirect(url_for('views.settings'))

    
    elif request.method == 'GET':
        # fills out the forms based on your current settings
        form.text_color.data = current_user.text_color
        form.text_size.data = current_user.text_size
        form.background.data = current_user.background

    return render_template("settings.html", User = User, user = current_user, username = current_user.username, form = form)


# frequently asked questions page
@views.route('/faq', methods = ['GET', 'POST'])
def faq():
    return render_template("faq.html", user = current_user)


# chat menu
@views.route('/', methods = ['GET', 'POST'])
@login_required
def chat():
    recipient = None    
    if request.method == 'POST':  #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category = 'error')
        else:
            new_message = Message(data = message, user_id = current_user.id)
            db.session.add(new_message)
            db.session.commit()  #update database

    # Get their username

    return render_template("chat_menu.html", User = User, user = current_user, username = current_user.username, 
        Message = Message, recipient = recipient, desc = desc, redirect = redirect, and_ = and_, or_ = or_, datetime = datetime)


# chat with a user selected
@views.route('/chat/<string:recipient>', methods = ['GET', 'POST'])
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
    
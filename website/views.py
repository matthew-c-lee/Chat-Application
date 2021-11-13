from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Message, Friend, Group, user_groups
from . import db
import json
from sqlalchemy import and_, desc
import secrets
import os
import datetime
from flask_wtf.file import FileField, FileAllowed
from PIL import Image
from .forms import RegistrationForm, LoginForm, UpdateAccountForm

views = Blueprint('views', __name__)

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


        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('views.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.status.data = current_user.status

    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', title='Account', image_file=image_file, form=form, user=current_user)

@views.route('/profile/<string:username>', methods=['GET', 'POST'])
@login_required
def other_profile(username):
    # user = User.query.get_or_404(username)
    
    user = User.query.filter(User.username == username).first_or_404()
    if user:
        image_file = url_for('static', filename='profile_pics/' + user.image_file)


    if request.method == 'POST':
        user.username = request.form['username']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('other_profile.html', user=user, image_file=image_file)

# Code for the Add Friend button
@views.route('/add-friend/<string:user_id>/<string:search>', methods=['GET', 'POST'])
@login_required
def add_friend(user_id, search):
    user = User.query.get(user_id)

    # if the user exists
    if user:
        new_friend = Friend(user_id=current_user.id, friend_id=user.id, friend_name=user.username)
        db.session.add(new_friend)
        db.session.commit()
        flash("You are now friends with " + user.username, category='success')
    return redirect("/search/" + search)

# Deletes messages
@views.route('/delete-message/<string:message_id>/<string:recipient_name>', methods=['GET', 'POST'])
def delete_message(message_id, recipient_name):
    message = Message.query.get(message_id)
    
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

    return redirect('/chat/' + recipient_name)

@views.route('/search/<string:search>', methods=['GET', 'POST'])
@login_required
def other_search(search):
    user_db = User.query.filter(User.username.like('%'+search+'%')).all()
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)


    return render_template("search.html", user=current_user, current_user=current_user, user_db = user_db, search=search, Friend=Friend, and_=and_)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user_db = None
    search = None
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)

    return render_template("search.html", user=current_user, current_user=current_user, user_db=user_db, search=search, Friend=Friend, and_=and_)

# settings
@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST': #if button is pressed
        current_user.text_color = request.form.get('textColor')
        current_user.text_size = request.form.get('textSize')
        current_user.background = request.form.get('background')
        db.session.commit()             

        flash('Settings were changed.', category='success')
        return render_template("settings.html", User=User, user=current_user, username=current_user.username)
               
    return render_template("settings.html", user=current_user)


@views.route('/faq', methods=['GET', 'POST'])
def faq():
        
    return render_template("faq.html", user=current_user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def chat():
    recipient = None    
    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()

    # Get their username
    user_db = User.query.all()
    message_db = Message.query.all()

    return render_template("chat.html", User=User, user=current_user, username=current_user.username, user_db=user_db, Message = Message, recipient=recipient, desc=desc, redirect=redirect)

@views.route('/chat/<string:recipient>', methods=['GET', 'POST'])
@login_required
def chat_with(recipient):
    recipient = User.query.filter(User.username == recipient).first_or_404()

    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id, recipient_id = recipient.id)
            db.session.add(new_message)
            db.session.commit()
            # flash('Message sent.', category='success')
            return redirect('/chat/' + recipient.username)


    # Get their username
    user_db = User.query.all()
    message_db = Message.query.all()

 
    return render_template("chat.html", User=User, user=current_user, username=current_user.username, user_db=user_db, Message = Message, recipient=recipient, desc=desc, redirect=redirect, message1=None, datetime=datetime)









# @views.route('/index')
# def index():
#     members = User.query.all()
#     return render_template('index.html', members=members)
    
# @views.route('/update', methods=['POST'])
# def update():

#     member = User.query.filter_by(id=request.form['id']).first()
#     member.username = request.form['name']
#     member.first_name = request.form['email']

#     db.session.commit()

#     return jsonify({'result' : 'success', 'member_num' : member.id})
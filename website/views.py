from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Message, Friend, Group, user_groups
from . import db
import json
from sqlalchemy import and_, desc
import secrets
import os
import datetime


views = Blueprint('views', __name__)

@views.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST': #if button is pressed
    # if request.form.get('status'):   # if there's anything typed in status bar
        status = request.form.get('status')

        if len(status) < 1:
            flash('Nothing changed.', category='error')
        else:
        
            flash("Status updated.", category='success')

            current_user.status = status   # change the user's status
            db.session.commit()   #update the database

    return render_template("profile.html", user=current_user)





@views.route('/profile/<string:username>', methods=['GET', 'POST'])
def other_profile(username):
    # user = User.query.get_or_404(username)
    user = User.query.filter(User.username == username).first_or_404()

    if request.method == 'POST':
        user.username = request.form['username']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'

    else:
        return render_template('other_profile.html', user=user)

@views.route('/add-friend/<string:user_id>/<string:search>', methods=['GET', 'POST'])
def add_friend(user_id, search):
    user = User.query.get(user_id)

    # if the user exists
    if user:
        new_friend = Friend(user_id=current_user.id, friend_id=user.id, friend_name=user.username)
        db.session.add(new_friend)
        db.session.commit()
        flash("You are now friends with " + user.username, category='success')
#         current_user.selected_friend = user      
    return redirect("/search/" + search)

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

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
        
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

    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db, Message = Message, recipient=recipient, desc=desc, redirect=redirect)

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

 
    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db, Message = Message, recipient=recipient, desc=desc, redirect=redirect, message1=None, datetime=datetime)









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
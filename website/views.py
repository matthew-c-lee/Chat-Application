from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Message, Friend, Group, Block, user_groups
from . import db
import json
from sqlalchemy import and_
import secrets
import os


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


@views.route('/create-group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group-name')
        
        if len(group_name) > 0:
            new_group = Group(group_name=group_name)
            new_group.members.append(current_user)
            db.session.add(new_group)
            db.session.commit()

        flash("Created " + group_name)

        # user = User.query.filter_by(username=username).first()
     
        
        # else:
        # new_group = Group(group_name=group_name)
        


        #     flash('Group created.', category='success')
        return redirect(url_for('views.chat'))

    # return render_template("sign_up.html", user=current_user)
    return render_template("create_group.html", user=current_user)


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
        return render_template('other_profile.html', user=user, current_user=current_user, and_=and_ , Block=Block)

@views.route('/add-friend/<string:user_id>/<string:search>', methods=['GET', 'POST'])
def add_friend(user_id, search):
    # user = json.loads(request.data)
    # userId = user['id']
    user = User.query.get(user_id)

    # if the user exists
    if user:
        new_friend = Friend(user_id=current_user.id, friend_id=user.id, friend_name=user.username)
        db.session.add(new_friend)
        db.session.commit()
        
        flash("You are now friends with " + user.username, category='success')
#         current_user.selected_friend = user      
    return redirect("/search/" + search)

@views.route('/add-block/<string:user_id>', methods=['GET', 'POST'])
def add_block(user_id):

    user = User.query.get(user_id)

    #friend = Friend.query.filter_by(Friend.user_id == current_user.id).first()
   #new_friend = Friend(user_id=current_user.id, friend_id=user.id, friend_name=user.username)
    #flash(new_friend)
   # if new_friend:
   #     db.session.delete(new_friend)
    #    db.session.commit()

    new_block = Block(user_id=current_user.id, blocked_id=user.id, blocked_name=user.username)
    old_friend = Friend.query.filter(Friend.user_id == current_user.id).first()
    db.session.add(new_block)
    db.session.commit()

    if old_friend:
        db.session.delete(old_friend)
        db.session.commit()


    flash("You have blocked " + user.username, category='success')

    return redirect(url_for('views.chat'))

@views.route('/remove-block/<string:user_id>', methods=['GET', 'POST'])
def remove_block(user_id):

    user = User.query.get(user_id)

    #new_block = Block(user_id=current_user.id, blocked_id=user.id, blocked_name=user.username)
    old_block = Block.query.filter(Block.user_id == current_user.id).first()
    db.session.delete(old_block)
    db.session.commit()
    
    flash("You have unblocked " + user.username, category='success')

    return redirect(url_for('views.chat'))

@views.route('/delete-message', methods=['POST'])
def delete_message():
    message = json.loads(request.data)
    messageId = message['messageId']
    message = Message.query.get(messageId)
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

    return jsonify({})

@views.route('/search/<string:search>', methods=['GET', 'POST'])
@login_required
def other_search(search):
    user_db = User.query.filter(User.username.like('%'+search+'%')).all()
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)


    return render_template("search.html", user=current_user, current_user=current_user, user_db = user_db, search=search, Friend=Friend, and_=and_, Block=Block)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user_db = None
    search = None
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)

    return render_template("search.html", user=current_user, current_user=current_user, user_db=user_db, search=search, Friend=Friend, and_=and_, Block=Block)

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
            # flash('Message sent.', category='success')

    # Get their username
    user_db = User.query.all()
    message_db = Message.query.all()

    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db, message_db = message_db, recipient=recipient)

@views.route('/chat/<string:recipient>', methods=['GET', 'POST'])
@login_required
def chat_with(recipient):
    recipient = User.query.filter(User.username == recipient).first_or_404()

    flash("You are now chatting with " + recipient.username, category='success')

    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id, recipient_id = recipient.id)
            db.session.add(new_message)
            db.session.commit()
            # flash('Message sent.', category='success')

    # Get their username
    user_db = User.query.all()
    message_db = Message.query.all()

 
    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db, message_db = message_db, recipient=recipient)

@views.route('/group-chat/<string:group_chat>', methods=['GET', 'POST'])
@login_required
def group_chat(group_chat):
    group = Group.query.filter(Group.group_name == group_chat).first_or_404()

    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id, group_id = group.group_id)
            db.session.add(new_message)
            db.session.commit()
            # flash('Message sent.', category='success')

    message_db = Message.query.all()
           
    return render_template("group_chat.html", user=current_user, username=current_user.username, user_db=User, message_db = message_db, group=group)

# page for adding members
@views.route('/add-members/<string:group_chat>', methods=['GET', 'POST'])
def add_members(group_chat):
    group = Group.query.filter(Group.group_name == group_chat).first_or_404()

    return render_template("add_members.html", user=current_user, group=group, db=db, user_groups=user_groups, and_=and_)

@views.route('/add-member/<string:group_id>/<string:member_id>', methods=['GET', 'POST'])
def add_member(group_id, member_id):
    group = Group.query.filter(Group.group_id == group_id).first_or_404()
    member = User.query.filter(User.id == member_id).first_or_404()

    in_group_already = db.session.query(user_groups).filter((user_groups.c.user_id==member.id) & (user_groups.c.group_id==group.group_id)).first()

    if member and not in_group_already:
        group.members.append(member)
        db.session.commit()

        flash("added " + member.username + " to " + group.group_name)
    else:
        flash(member.username + " is already in " + group.group_name, category="error")

    return redirect("/group-chat/" + group.group_name)


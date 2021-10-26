from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import Message
from . import db
import json
from .models import User

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

@views.route('/add-friend', methods=['GET', 'POST'])
def add_friend():
    user = json.loads(request.data)
    userId = user['id']
    user = User.query.get(userId)

    if user:
        flash("You are now friends with " + user.username, category='success')
#         current_user.selected_friend = user      
    return jsonify({})




# @views.route('/select-friend', methods=['POST'])
# def select_friend():
#     user = json.loads(request.data)
#     id = user['id']
#     user = User.query.get(id)
#     if user:
#         flash("You are now chatting with " + user.username, category='success')
#         current_user.selected_friend = user        

#     return jsonify({})



# @views.route('/friend-search', methods=['POST'])
# def friend_search():
#     user = json.loads(request.data)
#     id = user['id']
#     user = User.query.get(id)
#     if user:
#         flash("You are now chatting with " + user.username, category='success')

#     return jsonify({})

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


    return render_template("search.html", user=current_user, current_user=current_user, user_db = user_db, search=search)

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user_db = None
    search = None
    if request.form.get('search'):
        search = request.form.get('search')
        return redirect("/search/" + search)

    return render_template("search.html", user=current_user, current_user=current_user, user_db=user_db, search=search)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
        
    return render_template("settings.html", user=current_user)

@views.route('/', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent.', category='success')

    # Get their username
    user_db = User.query.all()
 
    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db)

@views.route('/chat/<string:chatter>', methods=['GET', 'POST'])
@login_required
def chat_with(chatter):
    chatter = User.query.filter(User.username == chatter).first_or_404()

    flash("You are now chatting with " + chatter.username, category='success')

    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id)
            db.session.add(new_message)
            db.session.commit()
            flash('Message sent.', category='success')

    # Get their username
    user_db = User.query.all()

 
    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db, chatter=chatter)
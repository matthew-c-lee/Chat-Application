from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Message
from . import db
import json
from .models import User

views = Blueprint('views', __name__)


# @views.route('/', methods=['GET', 'POST'])
# @login_required
# def home():
#     if request.method == 'POST': #if button is pressed
#         message = request.form.get('message')

#         if len(message) < 1:
#             flash('Message is too short', category='error')
#         else:
#             new_message = Message(data=message, user_id=current_user.id)
#             db.session.add(new_message)
#             db.session.commit()
#             flash('Message added.', category='success')
            
#     return render_template("home.html", user=current_user)

@views.route('/select-friend', methods=['POST'])
def select_friend():
    # flash("test", category='success')
    user = json.loads(request.data)
    id = user['id']
    user = User.query.get(id)
    if user:
        flash("You are now chatting with " + user.username, category='success')
        current_user.selected_friend = user        

        # if user.id == current_user.id:
        #     db.session.delete(message)
        #     db.session.commit()

    return jsonify({})

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

@views.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    user_db = None
    if request.form.get('search'):
        search = request.form.get('search')
    # flash(search, category='success')

    # user_db = User.query.all()
    # user_db = User.query.filter_by(username=search)
        user_db = User.query.filter(User.username.like('%'+search+'%')).all()


    return render_template("search.html", user=current_user, user_db = user_db)

@views.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
        
    return render_template("settings.html", user=current_user)

@views.route('/faq', methods=['GET', 'POST'])
@login_required
def faq():
        
    return render_template("faq.html", user=current_user)

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
    # flash(User.query.filter_by(username='Equivocus').all())

    # Get their username
    # for user in User:
    #     UserString = 
    # flash(User.query.filter_by(username='Equivocus').first().username)
    # user1 = User.query.filter_by(username='Equivocus').first().username
    # user1 = User.query.filter_by(username='Equivocus').first().username
    user_db = User.query.all()
    # selected_friend = 
    # flash(current_user.username, category='success')
    # current_user.username = "BananaMan"
    # if current_user:
    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db)
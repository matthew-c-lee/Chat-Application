from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .models import User

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': #if button is pressed
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')
            
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
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

@views.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    if request.method == 'POST': #if button is pressed
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note is too short', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added.', category='success')
    # flash(User.query.filter_by(username='Equivocus').all())

    # Get their username
    # for user in User:
    #     UserString = 
    # flash(User.query.filter_by(username='Equivocus').first().username)
    # user1 = User.query.filter_by(username='Equivocus').first().username
    # user1 = User.query.filter_by(username='Equivocus').first().username
    user_db = User.query.all()
    

            
    return render_template("chat.html", user=current_user, username=current_user.username, user_db=user_db)
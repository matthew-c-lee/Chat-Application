from flask import Blueprint, render_template, request, jsonify, redirect, url_for, jsonify
import json
from . import db

views = Blueprint(__name__, "views")

@views.route("/")
def home():
    return render_template("index.html", name="Joe", age=20)

# @views.route("/profile/<username>")
# def profile(username):
#     return render_template("index.html", name=username)

@views.route("/profile")
def profile():
    args = request.args
    name = args.get('name')
    return render_template("index.html", name=name)

@views.route("/json")
def get_json():
    return jsonify({'name':'tim', 'coolness':10})

@views.route("/data")
def get_data():
    data = request.json
    return jsonify(data)

@views.route("/go-to-home")
def go_to_home():
    return redirect(url_for("views.home"))

@views.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['note']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    
    return jsonify({})
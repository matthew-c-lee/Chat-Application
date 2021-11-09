from pytz import timezone
from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from .models import User, Message, Friend, Group, user_groups
from . import db
import json
from sqlalchemy import and_, desc
import secrets
import os
import datetime

group_views = Blueprint('group_views', __name__)

@group_views.route('/create-group', methods=['GET', 'POST'])
def create_group():
    if request.method == 'POST':
        group_name = request.form.get('group-name')
        
        if len(group_name) > 0:
            new_group = Group(group_name=group_name)
            new_group.members.append(current_user)
            db.session.add(new_group)
            db.session.commit()

        flash("Created " + group_name)
        group = Group.query.filter(Group.group_name == group_name)[-1]

        return redirect('/group-chat/' + str(group.group_id))

    return render_template("create_group.html", user=current_user)

@group_views.route('/change-group-name/<string:group_id>', methods=['GET', 'POST'])
def change_group_name(group_id):
    group = Group.query.filter(Group.group_id == group_id).first_or_404()

    if request.method == 'POST':
        new_name = request.form.get('group-name')
        
        if len(new_name) > 0:
            group.group_name = new_name
            db.session.commit()

        # flash("Created " + group_name)
        return redirect('/group-chat/' + str(group.group_id))

    return render_template("change_group_name.html", user=current_user)

# the actual group chat
@group_views.route('/group-chat/<string:group_id>', methods=['GET', 'POST'])
@login_required
def group_chat(group_id):
    # find the actual group from the name
    group = Group.query.filter(Group.group_id == group_id).first_or_404()

    if request.method == 'POST': #if button is pressed
        message = request.form.get('message')

        if len(message) < 1:
            flash('Message is too short.', category='error')
        else:
            new_message = Message(data=message, user_id=current_user.id, group_id = group.group_id)
            db.session.add(new_message)
            db.session.commit()
            # flash('Message sent.', category='success')
        return redirect('/group-chat/' + str(group.group_id))

    # east = timezone('US/Eastern')
           
    return render_template("group_chat.html", User=User, user=current_user, username=current_user.username, user_db=User, group=group, Message=Message, desc=desc, str=str, datetime=datetime)

# page for adding members
@group_views.route('/add-members/<string:group_chat>', methods=['GET', 'POST'])
def add_members(group_chat):
    group = Group.query.filter(Group.group_name == group_chat).first_or_404()

    return render_template("add_members.html", user=current_user, group=group, db=db, user_groups=user_groups, and_=and_)

@group_views.route('/add-member/<string:group_id>/<string:member_id>', methods=['GET', 'POST'])
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

    return redirect('/group-chat/' + str(group.group_id))

@group_views.route('/leave-group/<string:group_id>/<string:id>', methods=['GET', 'POST'])
@login_required
def leave_group(group_id, id):
    db.session.query(user_groups).filter(and_(user_groups.c.user_id == id, user_groups.c.group_id == group_id)).delete()
    db.session.commit()
    return redirect('/')

@group_views.route('/delete-message-group/<string:message_id>/<string:group_id>', methods=['GET', 'POST'])
def delete_message_group(message_id, group_id):
    message = Message.query.get(message_id)
    
    if message:
        if message.user_id == current_user.id:
            db.session.delete(message)
            db.session.commit()

    return redirect('/group-chat/' + str(group_id))

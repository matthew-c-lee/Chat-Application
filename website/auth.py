from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re

from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.chat'))
            else:
                flash('Incorrect password.', category='error')
        else:
            flash('User does not exist.', category='error')


    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        answer = request.form.get('answer')
        question = request.form.get('question')
        text_color='black'
        text_size='15px'
        background='white'

        user = User.query.filter_by(username=username).first()
     
        if user:
            flash('Username taken.', category='error')
        elif len(username) < 4:  # username is too short
            flash('Username must be at least 4 characters.', category='error')  # tell the user
        elif len(username) > 14:  # username is too long
            flash('Username must not exceed 14 characters.', category='error') 
        elif not(re.match(r'^\w+$', username)):
            flash('Username can only contain "_", no other special characters', category='error')
        elif re.search(r"\s", username):
            flash('Username cannot contain any spaces.', category='error')
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters.', category='error')
        elif not(re.search('[a-zA-Z]', password1)):
            flash('Password must contain at least one letter.', category='error')
        elif not(any(map(str.isdigit, password1))):
            flash('Password must contain at least one number.', category='error')
        elif password1.isalnum():
            flash('Password must contain at least one special character.', category='error')
        elif re.search(r"\s", password1):
            flash('Password must not contain any spaces.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(answer) < 1:
            flash('Security word must be at least 1 character', category='error')
        else:
            new_user = User(username=username, first_name=first_name, password=generate_password_hash(password1, method='sha256'), 
                            answer=answer, question=question, text_size=text_size, text_color=text_color, background=background)
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)

            flash('Account created.', category='success')
            return redirect(url_for('views.chat'))

    return render_template("sign_up.html", user=current_user)


@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        answer = request.form.get('answer')

        user = User.query.filter_by(username=username).first()
                  
        if user and not answer:
            return render_template("forgot_password_accept.html", user=current_user, username=user.username, question=user.question)
        elif user and (user.answer.lower() == answer.lower()):
            return redirect(url_for('auth.password_reset', user=current_user, username=user.username))
        else:
            flash('The user does not exist or your security word is incorrect.', category='error')

    return render_template("forgot_password.html", user=current_user)


    

@auth.route('/password-reset', methods=['GET', 'POST'])
def password_reset():
    if request.method == 'POST':
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        

        user = User.query.filter_by(username=username).first()

        print(username)
        print(user.text_size)
       
        
        if not user:
            flash('Write down your original username', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif len(password1) < 5:
            flash('Password must be at least 5 characters.', category='error')
        elif not(re.search('[a-zA-Z]', password1)):
            flash('Password must contain at least one letter.', category='error')
        elif not(any(map(str.isdigit, password1))):
            flash('Password must contain at least one number.', category='error')
        elif password1.isalnum():
            flash('Password must contain at least one special character.', category='error')
        elif re.search(r"\s", password1):
            flash('Password must not contain any spaces.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        else:
            user.password=generate_password_hash(password1, method='sha256')
            db.session.commit()
            flash('Password was reset successfully.', category='success')
            return redirect(url_for('views.chat'))

    return render_template("password_reset.html", user=current_user)   
    
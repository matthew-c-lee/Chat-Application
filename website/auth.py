from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
import re

from .models import User
from . import db
from .forms import RegistrationForm

auth = Blueprint('auth', __name__)

# Code for the login route
@auth.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':  # the user has attempted to login
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully.', category = 'success')
                login_user(user, remember = True)
                return redirect(url_for('views.chat'))
            else:
                flash('Incorrect password.', category = 'error')
        else:
            flash('User does not exist.', category = 'error')


    return render_template("login.html", user = current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

def validate_sign_up(username, password1, password2, answer):
    message = ''  # message that will be flashed to the screen

    is_validated = False

    if len(username) < 4:  # username is too short
        message = 'Username must be at least 4 characters.'  # tell the user
    elif len(username) > 14:  # username is too long
        message = 'Username must not exceed 14 characters.' 
    elif not(re.match(r'^\w+$', username)):
        message = 'Username can only contain "_", no other special characters'
    elif re.search(r"\s", username):
        message = 'Username cannot contain any spaces.'
    elif len(password1) < 7:
        message = 'Password must be at least 7 characters.'
    elif not(re.search('[a-zA-Z]', password1)):
        message = 'Password must contain at least one letter.'
    elif not(any(map(str.isdigit, password1))):
        message = 'Password must contain at least one number.'
    elif password1.isalnum():
        message = 'Password must contain at least one special character.'
    elif re.search(r"\s", password1):
        message = 'Password must not contain any spaces.'
    elif password1 !=  password2:
        message = 'Passwords do not match.'
    elif len(answer) < 1:
        message = 'Security word must be at least 1 character'
    else:
        is_validated = True

    return is_validated, message

@auth.route('/sign-up', methods = ['GET', 'POST'])
def sign_up():

    form = RegistrationForm()

    if form.validate_on_submit():

        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        answer = request.form.get('answer')
        question = request.form.get('security_question')
        text_color = 'black'
        text_size = '15px'
        background = 'white'

        user = User.query.filter_by(username = username).first()
        
        validated, message = validate_sign_up(username, password1, password2, answer)

    
        if validated and not user:

            new_user = User(username = username, password = generate_password_hash(password1, method = 'sha256'), 
                            answer = answer, question = question, text_size = text_size, text_color = text_color, background = background)
            
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember = True)

            flash('Account created.', category = 'success')
            return redirect(url_for('views.chat'))
        else:
            if user:
                message = 'Username taken.'

            flash(message, 'error')

    return render_template("sign_up.html", user = current_user, form = form)

@auth.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        username = request.form.get('username')
        answer = request.form.get('security_answer')

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
    
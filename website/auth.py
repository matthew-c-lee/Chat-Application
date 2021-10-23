from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.', category='success')
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

        user = User.query.filter_by(username=username).first()
     
        if user:
            flash('Username taken.', category='error')
        elif len(username) < 4:  # password too short
            flash('Username must be at least 4 characters.',
                  category='error')  # tell the user
        elif len(first_name) < 2:
            flash('First name must be at least 2 characters.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords do not match.', category='error')
        elif len(answer) < 1:
            flash('Security word must be at least 1 character', category='error')
        else:
            new_user = User(username=username, first_name=first_name, password=generate_password_hash(password1, method='sha256'), answer=answer)
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

        if user:
            if user.answer ==  answer:
                flash('Logged in successfully.', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.chat'))
            else:
                flash('Incorrect answer.', category='error')
        else:
            flash('User does not exist.', category='error')


    return render_template("forgot_password.html", user=current_user)

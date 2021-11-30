import re

from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, Form
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, AnyOf, NoneOf, InputRequired, Email
from .models import User

class RegistrationForm(FlaskForm):


    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=14)])
    password1 = PasswordField('password1', validators=[DataRequired(), Length(min=7, max=20)])
    password2 = PasswordField('password2', validators=[DataRequired(), EqualTo('password1', 'The passwords do not match.'), Length(min=7, max=20)])

    security_question = SelectField(u'Security Question', choices = [   'In what city were you born?', 
                                                                        'What was the name of your favorite pet?', 
                                                                        'What was the name of your first school?', 
                                                                        'What was the make of your first car?', 
                                                                        'What was your first job?'], validators = [DataRequired()])

    submit = SubmitField('Create Account')
    answer = StringField('Security Question Answer', validators=[DataRequired(), Length(min=2, max=20)])

    def validate_username(self, username):
        user = User.query.filter(User.username == username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')
        if not(re.match(r'^\w+$', username.data)):
            raise ValidationError('Username can only contain "_", no other special characters.')
        if re.search(r"\s", username.data):
            raise ValidationError('Username cannot contain any spaces.')

    def validate_password1(self, password1):
        password_requirements = 'Password must contain at least one letter, number, and special character.'

        if not(re.search('[a-zA-Z]', password1.data)):
            raise ValidationError(password_requirements)
        if not(any(map(str.isdigit, password1.data))):
            raise ValidationError(password_requirements)
        if password1.data.isalnum():
            raise ValidationError(password_requirements)
        if re.search(r"\s", password1.data):
            raise ValidationError('Password must not contain any spaces.')

class SettingsForm(FlaskForm):
    text_color = SelectField(u'Text Color', choices = ['Black', 'Blue', 'Green', 'Red', 'Orange'], validators = [DataRequired()])
    text_size = SelectField(u'Text Size', choices = ['Small', 'Medium', 'Large'], validators = [DataRequired()])
    background = SelectField(u'Message Background', choices = ['White', 'Grey', 'Orange'], validators = [DataRequired()])

    submit = SubmitField('Update')

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    submit = SubmitField('Update')
    status = StringField('Status', validators=[Length(max=80)])


    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. Please choose a different one.')

class UpdateGroupForm(FlaskForm):
    submit = SubmitField('Update')
    group_name = StringField('Group Name', validators=[Length(min=4, max=80)])
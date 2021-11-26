from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

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
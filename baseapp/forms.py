from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, HiddenField, IntegerField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo
from wtforms_components import DateField
from datetime import date

class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    username = StringField('Usersname', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50), Email()])

class UsersForm(FlaskForm):
    username = StringField('Usersname', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50), Email()])
    password = PasswordField('password', validators=[InputRequired(), Length(min=6, max=80),EqualTo('pwconfirm', message='Passwords must match')])
    pwconfirm = PasswordField('Repeat Password')
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])

class UsersFormEdit(FlaskForm):
    username = StringField('Usersname', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('Email', validators=[InputRequired(), Length(max=50), Email()])
    delete = HiddenField('Delete', default='N', validators=[Length(max=1)])

class UsersFormPassword(FlaskForm):
    password = PasswordField('New Password', validators=[InputRequired(), Length(min=6, max=80),EqualTo('pwconfirm', message='Passwords must match')])
    pwconfirm = PasswordField('Repeat New Password')


class LteForm(FlaskForm):
    input = IntegerField('Input Count', validators=[InputRequired()])
    archive = IntegerField('Input Count', validators=[InputRequired()])
    error = IntegerField('Input Count', validators=[InputRequired()])
    drop = IntegerField('Input Count', validators=[InputRequired()])
    location = StringField('Usersname', validators=[InputRequired(), Length(min=1, max=10)])
    date = DateField('Date',default=date.today(), format="%Y-%m-%d")
    

from flask_wtf import FlaskForm
from wtforms import  PasswordField
from wtforms import (StringField, BooleanField, DateTimeField,
                     RadioField,SelectField,TextField,
                     TextAreaField,SubmitField)
from wtforms.validators import DataRequired,Email,EqualTo
from wtforms import ValidationError
from flask_wtf.file import FileField,FileAllowed

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(),Email()])
    username = StringField('Username', validators=[DataRequired()])
    registration_number = StringField('registration_number', validators=[DataRequired()])
    Role = SelectField(u'Role',choices=[('Admin','Admin'),('User','User')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), EqualTo('pass_confirm', message='Passwords Must Match!')])
    pass_confirm = PasswordField('Confirm password', validators=[DataRequired()])
    submit = SubmitField('Register!')



class SearchForm(FlaskForm):
    DocumentType = RadioField('Please choose your file type:', choices=[('Pdf','pdf'),('Excel','Excel'),('Word','Word')])
    File = FileField(u'Select file', validators=[FileAllowed([ 'Pdf'])])
    Search_Methods = SelectField(u'Select Method',choices=[('Text','Search in Texts'),('Images','Search in images')], validators=[DataRequired()])
    Input = StringField('Input', validators=[DataRequired()])
    submit = SubmitField('Go!')



    def check_email(self, field):
        # Check if not None for that user email!
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Your email has been registered already!')

    def check_username(self, field):
        # Check if not None for that username!
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Sorry, that username is taken!')

# -*- coding: utf-8 -*-
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField, PasswordField, RadioField, SelectField


# class NameForm(Form):
#     name = StringField('What is your name?', validators=[Required()])
#     submit = SubmitField('Submit')

class LoginForm(Form):
    user_id = StringField('What is your number?', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')


class RegisterForm(Form):
    name = StringField('Name', validators=[DataRequired()])  # validators=[DataRequired()]用于验证用户是否填了
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm', validators=[DataRequired()])
    user_id = StringField('Please Enter your Student/Teacher Id', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('male', 'male'), ('female', 'female')], validators=[DataRequired()])
    class_name = StringField('Class', validators=[DataRequired()])
    role = SelectField('Role', choices=[('student', 'student'), ('teacher', 'teacher')], validators=[DataRequired()])
    # lesson = SelectField('Lesson', choices=[('1', 'Introductions to Computer Science'), ('2', 'Software Engeneer')])
    submit = SubmitField('Submit')

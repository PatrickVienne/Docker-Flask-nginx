# project/users/forms.py


from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class RegisterForm(Form):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=6, max=40)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=40)])
    confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])


from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import Required

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Enter Gameroom')

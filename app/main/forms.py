from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from wtforms.validators import ValidationError
from . import rooms

class LoginForm(FlaskForm):
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    password = PasswordField('Password')
    submit = SubmitField('Join Game')

    def validate_password(self, field):
        if any(x.get_room_name() == self.room.data for x in rooms.active_rooms):
            room = next((x for x in rooms.active_rooms if x.get_room_name() == self.room.data), None)
            if field.data != room.get_room_password():
                raise ValidationError("Password is incorrect")

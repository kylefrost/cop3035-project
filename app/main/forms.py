from flask_wtf import FlaskForm
from wtforms.fields import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from wtforms.validators import ValidationError
from . import rooms

# LoginForm class creates login on index page
class LoginForm(FlaskForm):
    # Create fields
    name = StringField('Name', validators=[Required()])
    room = StringField('Room', validators=[Required()])
    password = PasswordField('Password')
    submit = SubmitField('Join Game')

    # Valide password function checks if password is correct, also checks number of users in room
    def validate_password(self, field):
        if any(x.get_room_name() == self.room.data for x in rooms.active_rooms):
            room = next((x for x in rooms.active_rooms if x.get_room_name() == self.room.data), None)
            if field.data != room.get_room_password():
                raise ValidationError("Password is incorrect")
            if len(room.get_room_users()) == 8:
                raise ValidationError("Already 8 users in the room")

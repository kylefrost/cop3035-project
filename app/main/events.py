from flask import session, request
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import rooms, users

def getRoom(name):
    return next((x for x in rooms.active_rooms if x.get_room_name() == name), None)

def getUser(room, name):
    return next((x for x in room.get_room_users() if x.get_user_name() == name), None)

@socketio.on('connect', namespace='/game')
def on_connect():
    room = getRoom(session.get('room'))
    name = session.get('name')
    user = users.User(name, room.get_room_name(), request.sid)
    room.users.append(user)

@socketio.on('joined', namespace='/game')
def joined(message):
    room = getRoom(session.get('room'))
    user = getUser(room, session.get('name'))
    join_room(room.get_room_name())
    emit('set_storage', {'user': user.get_user_name()}, room=user.get_user_id())

@socketio.on('send_chat', namespace='/game')
def send_chat(user, message):
    room = getRoom(session.get('room'))
    user = getUser(room, user)
    print(user.get_user_id())
    emit('new_chat', {'user': user.get_user_name(), 'message': message}, room=room.get_room_name(), skip_sid=user.get_user_id())

@socketio.on('leave', namespace='/game')
def leave(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the game.'}, room=room)
    session.clear()

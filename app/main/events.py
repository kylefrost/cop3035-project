from flask import session
from flask_socketio import emit, join_room, leave_room
from .sql import Word
from .. import socketio

@socketio.on('joined', namespace='/game')
def joined(message):
    room = session.get('room')
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the game.'}, room=room)

@socketio.on('send_chat', namespace='/game')
def text(message):
    room = session.get('room')
    emit('message', {'msg': session.get('name') + ': ' + message['msg']}, room=room)

@socketio.on('leave', namespace='/game')
def leave(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the game.'}, room=room)
    session.clear()

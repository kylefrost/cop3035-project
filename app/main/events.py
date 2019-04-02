from flask import session, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import rooms, users

from time import sleep
from threading import Thread

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
    print("User " + user.get_user_name() + " has connected to room " + room.get_room_name() + ".")

@socketio.on('joined', namespace='/game')
def joined(message):
    room = getRoom(session.get('room'))
    user = getUser(room, session.get('name'))
    join_room(room.get_room_name())
    emit('set_storage', {'user': user.get_user_name()}, room=user.get_user_id())
    emit('new_chat', {'user': 'SERVER', 'message': user.get_user_name() + ' has joined the room.'}, room=room.get_room_name())
    users_list = []
    for u in room.get_room_users():
        users_list.append([u.get_user_name(), u.get_user_score()])
    emit('update_leaderboard', {'users': users_list}, room=room.get_room_name())
    

@socketio.on('send_chat', namespace='/game')
def send_chat(user, message):
    room = getRoom(session.get('room'))
    user = getUser(room, user)
    emit('new_chat', {'user': user.get_user_name(), 'message': message}, room=room.get_room_name(), skip_sid=user.get_user_id())

@socketio.on('start_timer',namespace='/game')
def start_timer(data):
    print('Starting game timer.')
    room = getRoom(session.get('room'))
    thread = Thread(target=timer, args=(room.get_room_name(),))
    thread.daemon = True
    thread.start()

def timer(room, seconds=60):
    for i in range(seconds):
        socketio.emit('update_timer', {'timer': i+1}, room=room, namespace='/game')
        sleep(1)

@socketio.on('leave', namespace='/game')
def leave(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the game.'}, room=room)
    session.clear()

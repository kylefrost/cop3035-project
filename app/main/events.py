from flask import session, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import rooms, users
from random import shuffle
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
    dice = [['R','I','F','O','B','X'],['I','F','E','H','E','Y'],['D','I','N','O','W','S'],['U','T','O','K','N','D'],['H','M','S','R','A','O'],['L','U','P','E','T','S'],['A','C','I','T','O','A'],['Y','L','G','K','U','E'],['Qu','B','M','J','O','A'],['E','H','I','S','P','N'],['V','E','T','I','G','N'],['B','A','L','I','Y','T'],['E','Z','A','V','N','D'],['R','A','L','E','S','C'],['U','W','I','L','R','G'],['P','A','C','E','M','D']]
    room = getRoom(session.get('room'))
    rolled_die=[]
    for die in dice:
        shuffle(die)
        rolled = die[0]
        rolled_die.append(rolled)
    emit("rolled_die", {'dice':rolled_die}, room=room.get_room_name())
    thread = Thread(target=timer, args=(room.get_room_name(),))
    thread.daemon = True
    thread.start()

def timer(room, seconds=60):
    for i in range(seconds):
        socketio.emit('update_timer', {'timer': i+1}, room=room, namespace='/game')
        sleep(1)
<<<<<<< HEAD
        
=======

@socketio.on('add_word', namespace='/game')
def add_word(user_name, word):
    room = getRoom(session.get('room'))
    user = getUser(room, user_name)
    user.add_word_to_list(word)

@socketio.on('end_game_words', namespace='/game')
def end_game_words(room):
    room = getRoom(session.get('room'))
    final_words = {}
    for user in room.get_room_users():
        final_words[user.get_user_name()] = user.get_word_list()    

>>>>>>> 0bef344997d2bdcd0ec9375300e23679ccc1f44d
@socketio.on('leave', namespace='/game')
def leave(message):
    room = session.get('room')
    leave_room(room)
    emit('status', {'msg': session.get('name') + ' has left the game.'}, room=room)
    session.clear()

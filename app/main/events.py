from flask import session, request, copy_current_request_context
from flask_socketio import emit, join_room, leave_room
from .. import socketio
from . import rooms, users
from .sql import Word
from random import shuffle
from time import sleep, strftime, gmtime
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
def send_chat(in_user, message):
    room = getRoom(session.get('room'))
    user = getUser(room, in_user)
    emit('new_chat', {'user': user.get_user_name(), 'message': message}, room=room.get_room_name(), skip_sid=user.get_user_id())

@socketio.on('get_ready', namespace='/game')
def get_ready(starting_user):
    room = getRoom(session.get('room'))
    user = getUser(room, starting_user)
    emit('get_ready_front', {'user': starting_user}, room=room.get_room_name())

@socketio.on('start_timer',namespace='/game')
def start_timer(data):
    print('Starting game timer.')
    dice = [['R','I','F','O','B','X'],['I','F','E','H','E','Y'],['D','I','N','O','W','S'],['U','T','O','K','N','D'],['H','M','S','R','A','O'],['L','U','P','E','T','S'],['A','C','I','T','O','A'],['Y','L','G','K','U','E'],['Qu','B','M','J','O','A'],['E','H','I','S','P','N'],['V','E','T','I','G','N'],['B','A','L','I','Y','T'],['E','Z','A','V','N','D'],['R','A','L','E','S','C'],['U','W','I','L','R','G'],['P','A','C','E','M','D']]
    room = getRoom(session.get('room'))
    rolled_die = []
    for die in dice:
        shuffle(die)
        rolled = die[0]
        rolled_die.append(rolled)
    emit("rolled_die", {'dice':rolled_die}, room=room.get_room_name())
    thread = Thread(target=timer, args=(room.get_room_name(),))
    thread.daemon = True
    thread.start()

def timer(room, seconds=60, end=-1, step=-1):
    for i in range(seconds, end, step):
        socketio.emit('update_timer', {'timer': strftime('%M:%S', gmtime(i))}, room=room, namespace='/game')
        sleep(1)
    socketio.emit('end_game', {}, room=room, namespace='/game')

@socketio.on('new_user_word', namespace='/game')
def new_user_word(user_name, input_word):
    room = getRoom(session.get('room'))
    user = getUser(room, user_name)
    if len(input_word) < 3:
        emit('play_error', {'error': 'Word must be longer than 3 letters.'}, room=user.get_user_id())
        return
    elif input_word in user.get_word_list():
        emit('play_error', {'error': 'Already played ' + input_word + '.'}, room=user.get_user_id())
        return
    elif Word.query.filter_by(word=input_word).first() is None:
        emit('play_error', {'error': input_word + ' is not a real word.'}, room=user.get_user_id())
        return
    emit('word_success', {'user': user.get_user_name(), 'word': input_word}, room=user.get_user_id())

@socketio.on('add_word', namespace='/game')
def add_word(user_name, word):
    room = getRoom(session.get('room'))
    user = getUser(room, user_name)
    user.add_word_to_list(word)
    print(user.get_user_name() + "'s word list:")
    print(user.get_word_list())

@socketio.on('end_game_words', namespace='/game')
def end_game_words(room):
    room = getRoom(session.get('room'))

    #master list
    roomList = []
    for user in room.get_room_users():
        roomList = roomList + user.get_word_list()

    #find duplicates in room list
    seen = set()
    dupes = set()
    for x in roomList:
        if x in seen and x not in dupes:
            dupes.add(x)
        else:
            seen.add(x)

    users_dict = {}
    for user in room.get_room_users():
        filtered = list(set(user.get_word_list()) - dupes)
        user.add_filtered_list(filtered)

        users_dict[user.get_user_name()] = (user.get_word_list(), user.get_filtered_list())

    emit('all_word_lists', users_dict, room=room.get_room_name())

    for user in room.get_room_users():
        print(user.get_user_name() + "'s filtered word list:")
        print(user.get_filtered_list())


@socketio.on('leave', namespace='/game')
def leave(data):
    room = getRoom(session.get('room'))
    user = getUser(room, session.get('name'))
    leave_room(room.get_room_name())
    room.remove_room_user(user.get_user_name())
    users_list = []
    for u in room.get_room_users():
        users_list.append([u.get_user_name(), u.get_user_score()])
    emit('update_leaderboard', {'users': users_list}, room=room.get_room_name())
    print(data['user'] + ' left the room.')
    emit('new_chat', {'user': 'SERVER', 'message': user.get_user_name() + ' has left the room.'}, room=room.get_room_name())
    session.clear()



def update_scores(room):
    end_game_words # Do I just call it? or should it be returning a dict of words per player?
    score_matrix = {3:1, 4:1, 5:2, 6:3, 7:5} # A word longer than 7 is worth 11 pts

    for player in room.get_room_users:
        for word in final_words[player]: # Not sure how to get this dict
            if len(word) > 7:
                player.round_score += 11
            else:
                player.round_score += score_matrix[len(word)]

        player.user_score += player.round_score
        player.round_score = 0

from flask import session, redirect, url_for, render_template, request
from . import main, rooms
from .forms import LoginForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        if any(x.get_room_name() == form.room.data for x in rooms.active_rooms):
            room = next((x for x in rooms.active_rooms if x.get_room_name() == form.room.data), None)
        else:
            rooms.active_rooms.append(rooms.Room(form.room.data, form.password.data, form.name.data))
        session['name'] = form.name.data
        session['room'] = form.room.data
        session['password'] = form.password.data
        return redirect(url_for('.game'))
    elif request.method == 'GET':
        pass
    return render_template('index.html', form=form)

@main.route('/game')
def game():
    print(rooms.active_rooms)
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('game.html', name=name, room=room)

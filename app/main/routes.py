from flask import session, redirect, url_for, render_template, request
from . import main
from .forms import LoginForm

@main.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        session['room'] = form.room.data
        session['password'] = form.password.data
        return redirect(url_for('.game'))
    elif request.method == 'GET':
        pass
    return render_template('index.html', form=form)

@main.route('/game')
def game():
    name = session.get('name', '')
    room = session.get('room', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('game.html', name=name, room=room)

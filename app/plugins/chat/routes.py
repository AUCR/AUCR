"""AUCR chat plugin route page handler."""
# coding=utf-8
from flask import Blueprint
from flask import session, redirect, url_for, render_template, request
from flask_login import current_user, login_required
from app.plugins.chat.forms import ChatForm
from app.plugins.chat import events

chat_page = Blueprint('chat', __name__, template_folder='templates')


@chat_page.route('/', methods=['GET', 'POST'])
@login_required
def chat_index():
    """Login form to enter a room."""
    form = ChatForm()
    if form.validate_on_submit():
        session['room'] = form.room.data
        return redirect(url_for('chat.chat_room'))
    elif request.method == 'GET':
        form.room.data = session.get('room', '')
    return render_template('index.html', form=form)


@chat_page.route('/room')
@login_required
def chat_room():
    """Chat room. The user's name and room must be stored in the session."""
    room = session.get('room', '')
    if room == '':
        return redirect(url_for('main.index'))
    return render_template('chat.html', name=current_user.username, room=room)

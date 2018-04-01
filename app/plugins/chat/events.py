"""AUCR chat plugin event handler."""
# coding=utf-8
from flask import session
from flask_login import current_user
from flask_socketio import emit, join_room, leave_room
from app import socketio, db
from app.plugins.chat.models import Chat


@socketio.on('joined', namespace='/room')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    join_room(room)
    if current_user.is_authenticated:
        emit('status', {'msg': current_user.username + ' has entered the room.'}, room=room)
        msg = Chat.__call__(author=current_user.username, message='has entered the room.', room=room)
        db.session.add(msg)
        db.session.commit()


@socketio.on('text', namespace='/room')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    if current_user.is_authenticated:
        emit('message', {'msg': current_user.username + ': ' + message['msg']}, room=room)
        msg = Chat.__call__(author=current_user.username, message=message['msg'], room=room)
        db.session.add(msg)
        db.session.commit()


@socketio.on('left', namespace='/room')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    room = session.get('room')
    leave_room(room)
    if current_user.is_authenticated:
        emit('status', {'msg': current_user.username + ' has left the room.'}, room=room)
        msg = Chat.__call__(author=current_user.username, message='has left the room.', room=room)
        db.session.add(msg)
        db.session.commit()

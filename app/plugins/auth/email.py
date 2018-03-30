"""AUCR auth plugin email handler."""
# coding=utf-8
from threading import Thread
from app import mail
from flask import current_app, render_template
from flask_babel import _
from flask_mail import Message


def send_async_email(app, msg):
    """Send_async_email function sends a message to a user."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, sender, recipients, text_body, html_body, attachments=None, sync=False):
    """Send_email function sends emails if you have it configured."""
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)
    if sync:
        mail.send(msg)
    else:
        try:
            Thread(target=send_async_email, args=(current_app.get_current_object(), msg)).start()
        except AttributeError:
            return msg


def send_password_reset_email(user):
    """"Send user password reset email."""
    token = user.get_reset_password_token()
    # TODO add a check if the user has a public key to encrypt before sending out
    send_email(_('[AUCR] Reset Your Password'),
               sender=current_app.config['ADMINS'][0], recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))

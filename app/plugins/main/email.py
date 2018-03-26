"""Email python script to send emails to people."""
# coding=utf-8
from threading import Thread
from app import mail
from flask import current_app
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

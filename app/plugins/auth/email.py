"""AUCR auth plugin email handler."""
# coding=utf-8
from flask import render_template, current_app
from flask_babel import _
from app.plugins.main.email import send_email


def send_password_reset_email(user):
    """"Send user password reset email."""
    token = user.get_reset_password_token()
    # TODO add a check if the user has a public key to encrypt before sending out
    send_email(_('[AUCR] Reset Your Password'),
               sender=current_app.config['ADMINS'][0], recipients=[user.email],
               text_body=render_template('email/reset_password.txt', user=user, token=token),
               html_body=render_template('email/reset_password.html', user=user, token=token))

"""AUCR auth routes manages all basic flask app blueprints."""
# coding=utf-8
import pyqrcode
import base64
import os
from io import BytesIO
from datetime import datetime
from flask import render_template, flash, Blueprint, session,  redirect, url_for, request, current_app, g, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from flask_babel import _
from app import db
from app.plugins.auth.forms import LoginForm, RegistrationForm, ResetPasswordRequestForm, ResetPasswordForm, \
     CreateGroupForm, RemoveUserFromGroup, MessageForm, EditProfileForm
from app.plugins.auth.email import send_password_reset_email
from app.plugins.auth.utils import check_group
from app.plugins.auth.models import Group, Message, User, Notification, Post
from app.plugins.errors.handlers import render_error_page_template

auth_page = Blueprint('auth', __name__, template_folder='templates')


@auth_page.route('/user/<username>')
@login_required
def user(username):
    """User function returns the username url path."""
    username = User.query.filter_by(username=username).first_or_404()
    # page = request.args.get('page', 1, type=int)
    return render_template('user.html', user=username)


@auth_page.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit profile function allows the user to modify their about me section."""
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        user_name = User.query.filter_by(username=current_user.username).first()

        if user_name.otp_secret:
            current_user.otp_secret = user_name.otp_secret
        else:
            current_user.otp_secret = base64.b32encode(os.urandom(64)).decode('utf-8')
        db.session.commit()
        flash(current_user.otp_secret)
        flash(_('Your user profile changes have been saved!'))
        return redirect(url_for('auth.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
        if form.otp_token_checkbox:
            if form.otp_token_checkbox.data:
                form.otp_token.data = current_user.otp_token
        else:
            form.otp_token_checkbox = current_user.otp_token_checkbox
    return render_template('edit_profile.html', title=_('Edit Profile'), form=form)


@auth_page.route('/messages')
@login_required
def messages():
    """Return user message flask app blueprint route."""
    current_user.last_message_read_time = datetime.utcnow()
    current_user.add_notification('unread_message_count', 0)
    db.session.commit()
    page = request.args.get('page', 1, type=int)
    messages_list = current_user.messages_received.order_by(Message.timestamp.desc()).paginate(
               page, current_app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('auth.messages', page=messages_list.next_num) if messages_list.has_next else None
    prev_url = url_for('auth.messages', page=messages_list.prev_num) if messages_list.has_prev else None
    return render_template('messages.html', messages=messages_list.items, next_url=next_url, prev_url=prev_url)


@auth_page.route('/send_message/<recipient>', methods=['GET', 'POST'])
@login_required
def send_message(recipient):
    """AUCR auth plugin function sends a message to an input recipient."""
    recipient_user = User.query.filter_by(username=recipient).first_or_404()
    form = MessageForm()
    if form.validate_on_submit():
        msg = Message.__call__(author=current_user, recipient=recipient_user, body=form.message.data)
        db.session.add(msg)
        recipient_user.add_notification('unread_message_count', recipient_user.new_messages())
        db.session.commit()
        flash(_('Your message has been sent.'))
        return redirect(url_for('auth.user', username=recipient))
    return render_template('send_message.html', title=_('Send Message'), form=form, recipient=recipient)


@auth_page.route('/notifications')
@login_required
def notifications():
    """Return user flask app blueprint route."""
    # TODO add this to get all recent notifications like updates from tasks
    since = request.args.get('since', 0.0, type=float)
    user_notifications = current_user.notifications.filter(
        Notification.timestamp > since).order_by(Notification.timestamp.asc())
    return jsonify([{'name': n.name, 'data': n.get_data(), 'timestamp': n.timestamp} for n in user_notifications])


@auth_page.route('/register', methods=['GET', 'POST'])
def register():
    """AUCR auth plugin user register flask blueprint."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.__call__(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        session['username'] = user.username
        return redirect(url_for('auth.login'))
    return render_template('register.html', title=_('Register'), form=form)


@auth_page.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    """AUCR auth plugin reset password request flask blueprint."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(_('If that is a valid email the instructions have been sent to reset your password'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password_request.html', title=_('Reset Password'), form=form)


@auth_page.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    """User reset password with token AUCR auth plugin blueprint."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('auth.login'))
    return render_template('reset_password.html', form=form)


@auth_page.route('/groups', methods=['GET', 'POST'])
@login_required
def groups():
    """AUCR group's route flask blueprints."""
    if check_group("admin") is True:
        group_info = Group.query.order_by(Group.group_name).all()
        form_remove_user_from_group = RemoveUserFromGroup
        return render_template('groups.html', group_info=group_info, form=form_remove_user_from_group)
    else:
        return render_error_page_template(403)


@auth_page.route('/create_group', methods=['GET', 'POST'])
@login_required
def create_group():
    """Create a new group."""
    if check_group("admin") is True:
        form = CreateGroupForm()
        if form.validate_on_submit():
            group_name = Group(group_name=form.group_name.data, username=form.admin_user.data)
            db.session.add(group_name)
            db.session.commit()
            group_create_message = str('The group ' + str(group_name.group_name) + ' has been created!')
            flash(_(group_create_message))
            return redirect(url_for('auth.groups'))
        return render_template('create_group.html', form=form)
    else:
        return render_error_page_template(403)


@auth_page.route('/remove_user_from_group', methods=['GET', 'POST'])
@login_required
def remove_user_from_group():
    """AUCR auth plugin group flask app blueprint to remove a user."""
    if check_group("admin") is True:
        form = RemoveUserFromGroup()
        if form.validate_on_submit():
            Group.query.filter_by(group_name=form.group_name.data, username=form.username.data).delete()
            db.session.commit()
            group_create_message = str('The user ' + str(form.username.data) +
                                       'has been removed from ' + str(form.group_name.data) + "!")
            flash(_(group_create_message))
            return redirect(url_for('auth.groups'))
        return render_template('remove_user_from_group.html', form=form)
    else:
        return render_error_page_template(403)


@auth_page.route('/twofactor')
def two_factor_setup():
    """Two factory auth user setup page."""
    if 'username' not in session:
        return redirect(url_for('main.index'))
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        return redirect(url_for('main.index'))
    # since this page contains the sensitive qrcode
    # make sure the browser does not cache it
    # flash(_('Congratulations, you are now a registered user! Please check your email to confirm the address'))
    # flash("Please use this token to setup your two-factor login \n" + user.otp_secret)
    return render_template('two-factor-setup.html'), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@auth_page.route('/qrcode')
def qrcode():
    """Two factor auth qrcode handling."""
    if 'username' not in session:
        render_error_page_template(404)
    user = User.query.filter_by(username=session['username']).first()
    if user is None:
        render_error_page_template(404)

    # for added security, remove username from session
    # render qrcode for FreeTOTP
    url = pyqrcode.create(user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=3)
    flash(user.otp_secret)
    del session['username']
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}


@auth_page.route('/login', methods=['GET', 'POST'])
def login():
    """Flask AUCR user login route."""
    if current_user.is_authenticated:
        # if user is logged in we get out of here
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.otp_secret is not None:
            otp_auth_check = user.verify_totp(form.token.data)
        else:
            otp_auth_check = True
        if user is None or not user.check_password(form.password.data) or otp_auth_check is False:
                user.verify_totp(form.token.data)
                flash('Invalid username, password or token.')
                return redirect(url_for('auth.login'))

        login_user(user, remember=form.remember_me.data)
        login_user(user)
        # log user in
        login_user(user)
        flash('You are now logged in!')
        return redirect(url_for('main.index'))
    return render_template('login.html', title=_('Sign In'), form=form)


@auth_page.route('/logout')
def logout():
    """Log user out and clear session data."""
    logout_user()
    return redirect(url_for('main.index'))


@auth_page.route('/search')
@login_required
def search():
    """AUCR search plugin flask blueprint."""
    if not g.search_form.validate():
        return redirect(url_for('search'))
    page = request.args.get('page', 1, type=int)
    posts, total = Post.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    messages, total = Message.search(g.search_form.q.data, page, current_app.config['POSTS_PER_PAGE'])
    next_url = url_for('search', q=g.search_form.q.data, page=page + 1) \
        if total > page * current_app.config['POSTS_PER_PAGE'] else None
    prev_url = url_for('search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
    return render_template('search.html', title=_('Search'), messages=messages, next_url=next_url, prev_url=prev_url,
                           posts=posts)

"""AUCR auth plugin default page forms."""
# coding=utf-8
from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, URL
from flask_babel import _, lazy_gettext as _l
from app.plugins.auth.models import User, Group, Groups


class LoginForm(FlaskForm):
    """Login User Form renders user login fields."""

    username = StringField(_l('Username'), validators=[DataRequired()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    token = StringField('Token')
    remember_me = BooleanField(_l('Remember Me'))
    submit = SubmitField(_l('Sign In'))


class RegistrationForm(FlaskForm):
    """Registration page Form class renders Fields for user registration."""

    username = StringField(_l('Username'), validators=[DataRequired()])
    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    website = StringField(_l('Website'))
    affiliation = StringField(_l('Affiliation'))
    country = StringField(_l('Country'))
    submit = SubmitField(_l('Register'))

    def validate_username(self, username):
        """Check registered username."""
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different username.'))

    def validate_email(self, email):
        """Ensure no duplicate emails."""
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(_('Please use a different email address.'))


class ResetPasswordRequestForm(FlaskForm):
    """Password reset flask form."""

    email = StringField(_l('Email'), validators=[DataRequired(), Email()])
    submit = SubmitField(_l('Request Password Reset'))


class ResetPasswordForm(FlaskForm):
    """Flask form field to reset password after email token auth."""

    password = PasswordField(_l('Password'), validators=[DataRequired()])
    password2 = PasswordField(_l('Repeat Password'), validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField(_l('Request Password Reset'))


class CreateGroupForm(FlaskForm):
    """Create groups flask app form field."""

    group_name = StringField(_l('Group Name'), validators=[DataRequired()])
    admin_user = IntegerField(_l('Admin ID'), validators=[DataRequired()])
    submit = SubmitField('Create the Group')

    def validate_admin_user(self, admin_user):
        """Validate proper permissions."""
        admin_user = User.query.filter_by(id=admin_user.data).first()
        if admin_user is None:
            raise ValidationError(_('Please use a different User Name as this is not a valid user'))

    def validate_group_name(self, group_name):
        """Check for free group name."""
        group_name = Groups.query.filter_by(name=group_name.data).first()
        if group_name:
            raise ValidationError(_('Please use a different Group name this name is taken'))


class RemoveUserFromGroup(FlaskForm):
    """Flask app form to remove user from a group."""

    group_name = StringField(_l('Group Name'), validators=[DataRequired()])
    username = StringField(_l('User Name'), validators=[DataRequired()])
    submit = SubmitField('Remove User From Group')

    def validate_group_name(self, group_name):
        """Check possible group duplicates."""
        group_name = Groups.query.filter_by(group_name=group_name.data).first()
        if group_name is None:
            raise ValidationError(_("Please use a different Group Name as we can't find that"))

    def validate_admin_user(self, group_name, username):
        """Check possible admin duplicates."""
        admin_user = Group.query.filter_by(group_name=group_name.data, username=username.data).first()
        if admin_user is not None:
            raise ValidationError(_('The selected user name is not in the selected group'))


class PostForm(FlaskForm):
    """Flask post form."""

    post = TextAreaField(_l('Say something'), validators=[DataRequired()])
    submit = SubmitField(_l('Submit'))


class EditProfileForm(FlaskForm):
    """Edit user profile settings."""

    # TODO make this allow the user to turn on and off the two factor auth and into a tabbed interface
    username = StringField(_l('Username'), validators=[DataRequired()])
    about_me = TextAreaField(_l('About me'), validators=[Length(min=0, max=140)])
    otp_secret = TextAreaField(_l('OTP Token'), validators=[Length(min=0, max=140)])
    otp_token_checkbox = BooleanField(default=False)
    submit = SubmitField(_l('Submit'))

    def __init__(self, original_username, *args, **kwargs):
        """Edit user profile init self and return username."""
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        """Return a validation error if username is taken."""
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError(_('Please use a different username.'))

    def validate_otp_checkbox(self):
        """Return a validation error if OTP set."""
        user = User.query.filter_by(username=self.username.data).first()
        if user.otp_secret is not None:
            flash(self.otp_secret)
            raise ValidationError(_('The OTP token has already been set.'))


class MessageForm(FlaskForm):
    """AUCR auth plugin flask app message form."""

    message = TextAreaField(_l('Message'), validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField(_l('Submit'))

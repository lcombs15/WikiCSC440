"""
    Forms
    ~~~~~
"""
from flask_wtf import Form
from wtforms import BooleanField
from wtforms import TextField
from wtforms import TextAreaField
from wtforms import PasswordField
from wtforms import HiddenField
from wtforms.validators import InputRequired
from wtforms.validators import ValidationError

from wiki.core import clean_url
from wiki.web import current_wiki
from wiki.web import current_users


class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if current_wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return clean_url(url)


class SearchForm(Form):
    term = TextField('', [InputRequired()])
    ignore_case = BooleanField(
        description='Ignore Case',
        # FIXME: default is not correctly populated
        default=True)


class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')


class LoginForm(Form):
    name = TextField('', [InputRequired()])
    password = PasswordField('', [InputRequired()])

    def validate_name(form, field):
        user = current_users.get_user(field.data)
        if not user:
            raise ValidationError('This username does not exist.')

    def validate_password(form, field):
        user = current_users.get_user(form.name.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')


#class ChangeTheme(Form):



class ChangePasswordForm(Form):
    username = HiddenField("Field1")
    old_password = PasswordField('', [InputRequired()])
    new_password = PasswordField('', [InputRequired()])
    verify_new = PasswordField('', [InputRequired()])

    @staticmethod
    def check_new_passwords(new_password, verify_new):
        """
                Checks a user's current password and verifies if the user's new password is correct.
                Examples:
                >>> ChangePasswordForm.check_new_passwords("example", "example")
                True

                :param new_password: new password to change to
                :param verify_new: new password to verify the user made no mistakes
                :return: whether the two new passwords match or not
                """
        if new_password != verify_new:
            return False
        return True

    def validate_old_password(form, field):
        user = current_users.get_user(form.username.data)
        if not user:
            return
        if not user.check_password(field.data):
            raise ValidationError('Username and password do not match.')

    def validate_verify_new(form, field):
        if not ChangePasswordForm.check_new_passwords(form.new_password.data, form.verify_new.data):
            raise ValidationError("Something is not correct")







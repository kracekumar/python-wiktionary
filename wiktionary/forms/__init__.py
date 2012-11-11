#! -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, PasswordField, FileField, validators
from flask.ext.wtf import Required


class LoginForm(Form):
    """ Form for login"""
    username = TextField("Wikimedia Username", validators=[Required("Username is mandatory")])
    password = PasswordField("Wikimedia Password", validators=[Required("Password is mandatory")])


class WiktionaryNewForm(Form):
    """ Form to submit to wikionary for creating new article """
    title = TextField("title", description="Title of the article", validators=[Required("Title is mandatory")])


class WiktionaryInlineSectionForm(Form):
    """ Inline Form to be returned
    All the fields will be added dynamically
    """
    @classmethod
    def add_attr(self, name, value):
        print self.__class__, name, value
        setattr(self.__class__, name, value)


def check_file_extension(form, field):
    if not field.data.filename.endswith(u'json'):
        raise validators.ValidationError('File must be JSON')


class UploadForm(Form):
    """Upload bulk JSON FILE
    """
    json = FileField(u'JSON file', [Required(), check_file_extension])

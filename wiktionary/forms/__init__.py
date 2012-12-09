#! -*- coding: utf-8 -*-

from flask.ext.wtf import Form, TextField, TextAreaField, PasswordField, FileField, SelectField, validators, IntegerField
from flask.ext.wtf import Required, Optional


class LoginForm(Form):
    """ Form for login"""
    username = TextField("Wikimedia Username", validators=[Required("Username is mandatory")])
    password = PasswordField("Wikimedia Password", validators=[Required("Password is mandatory")])


class WiktionaryNewForm(Form):
    """ Form to submit to wikionary for creating new article """
    title = TextField("title", description="Title of the article", validators=[Required("Title is mandatory")])
    template = SelectField(u'Template', description="Select to display no of fields dynamically", coerce=int)

    section_title = TextField("Section Title", description="Section Title", validators=[Required()])
    section_content = TextAreaField("Section Content", description="Section Content", validators=[Required()])


class WiktionaryNewTemplateForm(Form):
    """ Form to submit to wikionary for creating new article """
    name = TextField("title", description="Title of the article", validators=[Required("Title is mandatory")])
    length = IntegerField(u'Total Field', validators=[Required()])
    field_names = TextAreaField("Template title names separated by comma", validators=[Optional()])


class WiktionaryInlineSectionForm(Form):
    """ Inline Form to be returned
    All the fields will be added dynamically
    """
    @classmethod
    def add_attr(self, name, value):
        setattr(self.__class__, name, value)


def check_file_extension(form, field):
    if not field.data.filename.endswith(u'json'):
        raise validators.ValidationError('File must be JSON')


class UploadForm(Form):
    """Upload bulk JSON FILE
    """
    json = FileField(u'JSON file', [Required(), check_file_extension])

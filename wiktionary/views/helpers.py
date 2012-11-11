#! -*- coding: utf-8 -*-

from flask import render_template, request, redirect, Markup, json
import flask.ext.wtf as wtf
from flask.ext.wtf import TextAreaField, TextField, Required
from wiktionary.forms import WiktionaryInlineSectionForm


class Count(object):
    start = 0
    count = start


def render_redirect(url, code=302):
    if request.is_xhr:
        return render_template('redirect.html', quoted_url=Markup(json.dumps(url)))
    else:
        return redirect(url, code=code)


def render_form(form, title, message='', formid='form', submit=u"Submit", cancel_url=None, ajax=False):
    multipart = False
    for field in form:
        if isinstance(field.widget, wtf.FileInput):
            multipart = True
    if request.is_xhr and ajax:
        return render_template('ajaxform.html', form=form, title=title,
            message=message, formid=formid, submit=submit,
            cancel_url=cancel_url, multipart=multipart)
    else:
        return render_template('autoform.html', form=form, title=title,
            message=message, formid=formid, submit=submit,
            cancel_url=cancel_url, ajax=ajax, multipart=multipart)


def generate_inline_form():
    class Temp(WiktionaryInlineSectionForm):
        pass
    suffix = Count.count
    setattr(Temp, u"title_" + unicode(suffix), TextField("Title", validators=[Required()]))
    setattr(Temp, u"content_" + unicode(suffix), TextAreaField("Content", validators=[Required()]))
    Count.count += 1
    return Temp, suffix

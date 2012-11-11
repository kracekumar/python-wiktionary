#! -*- coding: utf-8 -

from flask import (render_template, url_for, escape, flash, request, session, g, redirect,
    jsonify)

from wiktionary import app
from .helpers import render_form, generate_inline_form, render_redirect
from .api import login as l
from .api import LoginFailedError, get_current_url, post
from wiktionary.forms import LoginForm, WiktionaryNewForm, UploadForm


LINE_SPACE = """
"""


def check_login():
    try:
        if session['user']:
            return redirect(url_for('index'))
    except KeyError:
        return redirect(url_for('login', next=get_current_url))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    check_login()
    form = LoginForm()
    if form.validate_on_submit():
        username = escape(form.username.data)
        password = escape(form.password.data)
        try:
            l(username, password)
            flash(u"%s Successfully logged in" % (username), category="success")
        except LoginFailedError as e:
            flash(e.message, category="error")
        try:
            next = request.args.get('next', '')
        except Exception, e:
            pass
        if next:
            return redirect(url_for(next))
        return render_template('index.html')
    return render_form(form=form, title='Login', submit=u'Login',
        cancel_url=url_for('index'), ajax=False)


@app.route('/logout')
def logout():
    g.user = None
    session.pop('user', None)
    flash(u"Successfully logged out", "success")
    return redirect(url_for('index'))


@app.route('/new', methods=['POST', 'GET'])
def new():
    check_login()
    form = WiktionaryNewForm()
    if form.validate_on_submit():
        s = set([])
        for key in request.form:
            # FIXME: document
            val = request.form[key]
            if key == u'title':
                title = unicode(val)
            else:
                if u"_" in unicode(key):
                    k = key.split('_')
                    try:
                        s.add(int(k[-1]))
                    except ValueError:
                        pass
        result = sorted(s)
        text = title + LINE_SPACE
        for x in xrange(result[0], result[-1] + 1):
            try:
                text  += "===" + request.form[u'title_' + unicode(x)] + "===" + LINE_SPACE + request.form[u'content_' + unicode(x)] + LINE_SPACE
            except KeyError:
                pass
        # Post to mediawiki
        post({u'action': u'edit', u'title': title, u'action': 'edit', u'section': u'new', u'text': text})
        flash("Added page %s " % (title), "success")
        return render_redirect(url_for('index'))
    return render_template('new_wiktionary.html', form=form, title='Create',
        submit=u'Create', cancel_url=url_for('index'), ajax=False)


@app.route('/get_inline_form')
def return_inline_form():
    check_login()
    form, suffix = generate_inline_form()
    return jsonify({'code': render_template('section_title_content.html', form=form(), suffix=suffix)})


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    check_login()
    form = UploadForm()
    if form.validate_on_submit():
        content = r['json'].stream.read()
    return render_form(form=form, title='Upload Bulk wiktionary json file', submit=u'Login',
        cancel_url=url_for('index'), ajax=False)

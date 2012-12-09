#! -*- coding: utf-8 -

from flask import (render_template, url_for, escape, flash, request, session, redirect,
     json, jsonify, send_file)
#import gevent
#from gevent import monkey
#monkey.patch_all()
#
import sys
from baseframe.forms import render_form

from wiktionary import app
from .helpers import render_redirect
from .api import login as l
from .api import LoginFailedError, get_current_url, post
from wiktionary.forms import LoginForm, WiktionaryNewForm, UploadForm, WiktionaryNewTemplateForm
from wiktionary.models import Template, db


LINE_SPACE = """
"""

TITLE_SEPARATOR = u"===="


def parse_json(stream):
    return json.loads(stream)


def check_login():
    try:
        if session['username']:
            return None
        else:
            return redirect(url_for('login', next=get_current_url()), code=302)
    except KeyError:
        return redirect(url_for('login', next=get_current_url()), code=302)


@app.route('/')
def index():
    return render_template('index.html', host=app.config['MEDIAWIKI']['host'])


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
            return redirect(next)
        return render_template('index.html')
    return render_form(form=form, title='Login', submit=u'Login',
        cancel_url=url_for('index'), ajax=False)


@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('password', None)
    flash(u"Successfully logged out", "success")
    return redirect(url_for('index'))


@app.route('/new_template', methods=['POST', 'GET'])
def new_template():
    form = WiktionaryNewTemplateForm()
    if form.validate_on_submit():
        template = Template()
        form.populate_obj(template)
        db.session.add(template)
        db.session.commit()
        flash("Added %s" % (template.name), "success")
        return render_redirect(url_for('index'))
    return render_form(form=form, title='Create',
        submit=u'Create', cancel_url=url_for('index'), ajax=False)


@app.route('/new', methods=['POST', 'GET'])
def new():
    check_login()
    form = WiktionaryNewForm()
    all = Template.query.all()
    if all:
        form.template.choices, form.template.field_names = [], []
        for item in all:
            form.template.choices.append((item.length, item.name + "-" + unicode(item.length)))
            form.template.field_names.append((item.name, item.field_names))
    else:
        form.template.choices = [("General - 4", 4)]
    if form.validate_on_submit():
        title = request.form.get('title')
        section_titles = request.form.getlist('section_title')
        section_contents = request.form.getlist('section_content')
        text = u""
        for s_title, desc in zip(section_titles, section_contents):
            text += TITLE_SEPARATOR + s_title + TITLE_SEPARATOR + LINE_SPACE + desc + LINE_SPACE
        # Post to mediawiki
        try:
            result = post({u'action': u'edit', u'title': title, u'action': 'edit', u'section': u'new', u'text': text})
        except:
            return jsonify({'msg_type': u'failure', 'msg': u'Something Went wrong'})
        if u'error' in result:
            return jsonify({'url': url_for('new'),
                'msg': result[u'error'][u'info'],
                'msg_type': u'failure'})
        elif u'edit' in result:
            return jsonify({'url': url_for('index'),
                'msg': u'Added page %s ' % (title),
                'msg_type': u'success'})
    return render_template('new_wiktionary.html', form=form, title='Create',
        submit=u'Create', cancel_url=url_for('index'), ajax=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    r = check_login()
    if r is not None:
        return r
    form = UploadForm()
    if form.validate_on_submit():
        content = parse_json(unicode(form.json.data.stream.getvalue(), encoding="utf-8"))
        try:
            jobs = [(post(item), item) for item in content['items']]
            #jobs = [gevent.spawn(post, item) for item in content['items']]
            #gevent.joinall(jobs)
            #flash("All json objects posted - gevent", "success")
        except:
            flash("Something Wentwrong")
        return render_template('upload.html', jobs=jobs)
    return render_form(form=form, title='Upload Bulk wiktionary json file', submit=u'Upload',
        cancel_url=url_for('index'), ajax=False)


@app.route('/download', methods=['GET'])
def download():
    # there is a issue with this file in server so placing an try/catch block
    try:
        return send_file(app.config['SAMPLE_FILE_PATH'], as_attachment=True, attachment_filename='wiktionary_upload_sample.json')
    except IOError, e:
        print(e.args)

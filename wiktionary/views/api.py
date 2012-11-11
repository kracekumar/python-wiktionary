#! -*- coding: utf-8 -*-

from functools import wraps
from flask import flash, redirect, request, url_for, session
from wiktionary import app
from mwapi import MWApi


class User(object):
    def __init__(self, username, password, edittoken, watchtoken):
        self.username = username
        self.password = password
        self.edittoken = edittoken
        self.watchtoken = watchtoken


class LoginFailedError(Exception):
    pass


def get_current_url():
    """
    Return the current URL including the query string as a relative path.
    """
    url = url_for(request.endpoint, **request.view_args)
    query = request.environ.get('QUERY_STRING')
    if query:
        return url + '?' + query
    else:
        return url


def login(username, password):
    try:
        mw = MWApi(host=app.config['MEDIAWIKI']['host'],
            api_path=app.config['MEDIAWIKI']['api'])
        mw.login(username, password)
        mw.populateTokens()
        user = User(username, password, edittoken=mw.tokens['edittoken'],
            watchtoken=mw.tokens['watchtoken'])
        session['username'] = user.username
        session['password'] = user.password
        return mw
    except:
        raise LoginFailedError("Unable to Login")


def post(data):
    try:
        mw = login(session['username'], session['password'])
        mw.post({u'action': data['action'], u'token': mw.tokens['edittoken'], u'section': u'new', u'text': data['text'],
        u'title': data['title']})
    except:
        flash("Failed to upload %s" % data['title'], "error")

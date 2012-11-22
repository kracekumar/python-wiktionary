#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import os
import sys
from wiktionary import app, init
from wiktionary.models import db


try:
    app.config.from_pyfile('settings.py')
except IOError:
    print >> sys.stderr, "Did not find settings.py file in instance directory"

init()
db.create_all()
if app.config['ENVIRONMENT'] == u'dev':
    app.run(app.config['IP'], app.config['PORT_NO'], debug=True)
elif app.config['ENVIRONMENT'] == u'gevent':
    from gevent import wsgi
    ADMINS = ['kracethekingmaker@example.com']
    if not app.debug:
        import logging
        #from logging.handlers import SMTPHandler
        #mail_handler = SMTPHandler('127.0.0.1',
        #                           'me@kracekumar.com',
        #                           ADMINS, 'Wiktionary crashed')
        #mail_handler.setLevel(logging.ERROR)
        logger = logging.getLogger('wiktionary.log')
        logger.setLevel(logging.ERROR)
        app.logger.addHandler(logger)
    try:
        port = int(os.getenv("PORT"))
        if port:
            app.config['PORT_NO'] = port
    except:
        pass
    server = wsgi.WSGIServer((app.config['IP'], app.config['PORT_NO']), app)
    server.serve_forever()
else:
    pass

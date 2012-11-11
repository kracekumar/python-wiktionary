#! /usr/bin/env python
#! -*- coding: utf-8 -*-

import sys
from wiktionary import app, init
from wiktionary.models import db

try:
    app.config.from_pyfile('settings.py')
except IOError:
    print >> sys.stderr, "Did not find settings.py file in instance directory"

if app.config['ENVIRONMENT'] == u'dev':
    init()
    db.create_all()
    app.run('0.0.0.0', app.config['PORT_NO'], debug=True)

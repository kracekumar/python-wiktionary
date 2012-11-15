#! /usr/bin/env python
#! -*- coding: utf-8 -*-


from m2wsgi.io.standard import WSGIHandler
from wiktionary import app

zmq_port = "tcp://127.0.0.1:9999"
handler = WSGIHandler(app, zmq_port)
handler.serve()

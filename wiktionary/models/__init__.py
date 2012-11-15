#! -*- coding: utf-8 -*-

from flask.ext.sqlalchemy import SQLAlchemy
from wiktionary import app

db = SQLAlchemy(app)


class Template(db.Model):
    __tablename__ = 'template'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode(256), nullable=False, unique=True)
    length = db.Column(db.Integer, nullable=False, default=2)

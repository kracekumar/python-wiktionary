#! -*- coding-utf-8 -*-

from flask import Flask
from flask.ext.assets import Environment, Bundle


# initialize the app
app = Flask(__name__, instance_relative_config=True)

assets = Environment(app)

js = Bundle('js/libs/jquery-1.8.2.js',
    'js/libs/bootstrap.js',
    'js/lib/jquery.form.js',
    filters='jsmin', output='js/packed.js')

css = Bundle('css/bootstrap.min.css',
    'css/app.css',
    'css/jquery.ime.css',
    'css/toastr.css',
    filters='cssmin',
    output='css/packed.css')


def init():
    #configure the assests
    assets.register('js_all', js)
    assets.register('css_all', css)


import wiktionary.views
import wiktionary.forms

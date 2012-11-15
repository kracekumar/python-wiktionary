#! -*- coding-utf-8 -*-

from flask import Flask
from flask.ext.assets import Environment, Bundle
from baseframe import baseframe, baseframe_css, toastr_css, baseframe_js

# initialize the app
app = Flask(__name__, instance_relative_config=True)
app.register_blueprint(baseframe)

assets = Environment(app)

js = Bundle(baseframe_js,
    #'js/libs/bootstrap.js',
    #'js/libs/jquery-1.8.2.min.js',
    #'js/libs/toastr.js',
    #'js/libs/jquery.form.js',
    #'js/libs/jquery.ime.js',
    #'js/libs/jquery.ime.selector.js',
    #'js/libs/jquery.ime.preferences.js',
    #'js/libs/jquery.ime.inputmethods.js',
    filters='jsmin', output='js/packed.js')

css = Bundle(baseframe_css,
    toastr_css,
    'css/jquery.ime.css',
    'css/app.css',
    filters='cssmin',
    output='css/packed.css')


def init():
    #configure the assests
    assets.register('js_all', js)
    assets.register('css_all', css)


import wiktionary.views
import wiktionary.models
import wiktionary.forms

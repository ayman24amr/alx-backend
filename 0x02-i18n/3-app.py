#!/usr/bin/env python3
"""
starts a Flask web application
"""

from flask import Flask, render_template, request
from flask_babel import Babel


class Config(object):
    """
    Configuration class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)
babel = Babel(app)


@babel.localeselector
def get_locale():
    """get locale"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route("/", strict_slashes=False)
def index():
    """renders Hello world"""
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

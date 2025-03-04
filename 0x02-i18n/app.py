#!/usr/bin/env python3
"""
starts a Flask web application
"""

import datetime
from flask import Flask, render_template, request, g
from flask_babel import Babel, format_datetime
import pytz


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
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


def get_user(id):
    """gets a user"""
    return users.get(int(id), None)


@app.before_request
def before_request():
    """finds a user if any, and set it as a global on flask.g.user"""
    id = request.args.get('login_as', 0)
    setattr(g, 'user', get_user(id))
    setattr(g, 'time', format_datetime(datetime.datetime.now()))


@babel.localeselector
def get_locale():
    """get locale"""
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    if g.user:
        return g.user.get('locale')
    locale = request.accept_languages.best_match(app.config['LANGUAGES'])
    if locale:
        return locale
    return Config.BABEL_DEFAULT_LOCALE


@babel.timezoneselector
def get_timezone():
    """get timezone"""
    timezone = request.args.get('timezone', '').strip()
    if timezone:
        try:
            return pytz.timezone(timezone).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    if g.user:
        try:
            return pytz.timezone(g.user['timezone']).zone
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return app.config['BABEL_DEFAULT_TIMEZONE']


@app.route("/", strict_slashes=False)
def index():
    """renders Hello world"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')

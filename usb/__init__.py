from flask import Flask

from usb.models import db
from usb.blueprints.api import api
from usb.shortener import Shortener


def create_application(config_filename):
    """
    Application factory
    :param config_filename: Relative file path to pythonic config file
    :return: Application instance
    :rtype: flask.Flask
    """
    # Create and configure an application
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    # Init DB
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(api)

    # Add shortener
    app.shortener = Shortener(
        app.config['HASHIDS_SECRET'],
        app.config['SHORT_URL_MIN_LENGTH']
    )

    return app

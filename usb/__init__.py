from flask import Flask

from usb.models import db


def create_application(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)

    return app

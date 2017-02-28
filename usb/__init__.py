from flask import Flask

from usb.models import db
from usb.blueprints.api import api


def create_application(config_filename):
    app = Flask(__name__)
    app.config.from_pyfile(config_filename)

    db.init_app(app)

    app.register_blueprint(api)

    return app

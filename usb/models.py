import enum

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func

from sqlalchemy_utils.types import ChoiceType

db = SQLAlchemy()


class DeviceType(enum.Enum):

    DESKTOP = 0
    TABLET = 1
    MOBILE = 2


class Redirect(db.Model):

    __tablename__ = 'redirect'

    id = db.Column(db.Integer(), primary_key=True)
    short = db.Column(db.String(255))
    type = db.Column(ChoiceType(DeviceType, impl=db.SmallInteger()))
    url = db.Column(db.String(1024))
    datetime = db.Column(db.DateTime(timezone=True), default=func.now())
    count = db.Column(db.Integer(), default=0)

    def __init__(self, short_id, type, url):
        # TODO: maybe use `short_id` in db too?
        self.short = short_id
        self.type = type
        self.url = url

from flask_sqlalchemy import SQLAlchemy

from sqlalchemy.sql import func
from sqlalchemy.orm import synonym


db = SQLAlchemy()


class Redirect(db.Model):

    __tablename__ = 'redirect'

    id = db.Column(db.Integer(), primary_key=True)
    short = db.Column(db.String(255))
    _type = db.Column('type', db.SmallInteger())
    url = db.Column(db.String(1024))
    _datetime = db.Column('datetime', db.DateTime(timezone=True), default=func.now())
    count = db.Column(db.Integer(), default=0)

    def __init__(self, short_id, type, url, datetime=None, count=None):
        # TODO: maybe use `short_id` in db too?
        self.short = short_id
        self.type = type
        self.url = url
        if datetime is not None:
            self.datetime = datetime
        if count is not None:
            self.count = count

    @property
    def type(self):
        # TODO: getattr?
        return self.TYPE_STRING

    @type.setter
    def type(self, type):
        self._type = type

    type = synonym('_type', descriptor=type)

    @property
    def datetime(self):
        return self._datetime.isoformat()

    @datetime.setter
    def datetime(self, datetime):
        self._datetime = datetime

    datetime = synonym('_datetime', descriptor=datetime)

    __mapper_args__ = {
        'polymorphic_on': _type
    }


class DesktopRedirect(Redirect):

    TYPE_CODE = 0
    TYPE_STRING = 'desktop'

    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': TYPE_CODE
    }

    def __init__(self, short_id, url, datetime=None, count=None):
        super(DesktopRedirect, self).__init__(short_id, self.TYPE_CODE, url, datetime, count)


class TabletRedirect(Redirect):

    TYPE_CODE = 1
    TYPE_STRING = 'tablet'

    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': TYPE_CODE
    }

    def __init__(self, short_id, url, datetime=None, count=None):
        super(TabletRedirect, self).__init__(short_id, self.TYPE_CODE, url, datetime, count)


class Mobile(Redirect):

    TYPE_CODE = 2
    TYPE_STRING = 'mobile'

    __tablename__ = None

    __mapper_args__ = {
        'polymorphic_identity': TYPE_CODE
    }

    def __init__(self, short_id, url, datetime=None, count=None):
        super(Mobile, self).__init__(short_id, self.TYPE_CODE, url, datetime, count)



#!/usr/bin/env python

from flask_script import Manager
from flask_script.commands import ShowUrls

from usb import create_application
from usb.models import db

app = create_application('config/base.py')

manager = Manager(app, with_default_commands=True)
manager.add_command('show-urls', ShowUrls)


@manager.shell
def make_shell_context():
    """
    Add several handy imports for python shell
    """
    return {'app': app, 'db': db}


@manager.command
def createdb():
    """
    Create the database with all necessary structures
    """
    db.create_all()


@manager.command
def dropdb():
    """
    Drop all tables in the database
    """
    db.drop_all()

if __name__ == '__main__':
    manager.run()

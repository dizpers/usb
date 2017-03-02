import os

# Disable debug mode
DEBUG = False

# Disable testing mode
TESTING = False

# Set secret key
SECRET_KEY = 'H*&HD@*H#hhfhefw0083*(@#*(J@*#(JF8378'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'usb.db')

SERVER_NAME = 'jooraccess.com'

# Domain to build short link
SHORT_URL_DOMAIN = SERVER_NAME

# Secret key used to generate a hash
HASHIDS_SECRET = 'DJ(*#DJ(*@#JD((@J#!)JD#(JD#FHHF('

# Short length of a generated hash
SHORT_URL_MIN_LENGTH = 8

# Don't track modifications
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Redirect code - 301 or 302
REDIRECT_CODE = 301

try:
    from usb.config.local import *
except ImportError:
    pass

import os

# Disable debug mode
DEBUG = False

# Disable testing mode
TESTING = False

# Set secret key
SECRET_KEY = 'H*&HD@*H#hhfhefw00838378'

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'usb.db')

SERVER_NAME = 'jooraccess.com'

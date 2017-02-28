import tempfile

from usb.config.base import *

db_file = tempfile.NamedTemporaryFile()

# Enable debug mode
DEBUG = True

# Enable testing mode
TESTING = True

DATABASE_URI = 'sqlite:///' + db_file.name

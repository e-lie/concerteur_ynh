from app import *
from os import environ

application = create_app(environ['APP_SETTINGS'])


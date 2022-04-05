import os
import re
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    uri = os.getenv("DATABASE_URL")  # or other relevant config var
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    if uri.startswith("sqlite:///"):
        uri = 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
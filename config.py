import os
import re
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    #https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
    # uri = os.getenv("DATABASE_URL")  
    # if uri.startswith("postgres://"):
    #     uri = uri.replace("postgres://", "postgresql://", 1)
    # SQLALCHEMY_DATABASE_URI = uri or 'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'db.sqlite')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
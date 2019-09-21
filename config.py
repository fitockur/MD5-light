import os


basedir = os.path.abspath(os.path.dirname(__file__)) # base dir of the app


class Config(object):
    # CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i-wanna-work-in-bostongene'
    # dir of rhe database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # switch off tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False
import os


basedir = os.path.abspath(os.path.dirname(__file__)) # base dir of the app


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'i-wanna-work-in-bostongene'
    # dir of the database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')

    # switch off tracking
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    """
    SET ENVIRONMENT IN TERMINAL EXAMPLE
    >>> export MAIL_SERVER=smtp.googlemail.com
    >>> export MAIL_PORT=587
    >>> export MAIL_USE_TLS=1
    >>> export MAIL_USERNAME=<your-gmail-username>
    >>> export MAIL_PASSWORD=<your-gmail-password>
    """
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS') is not None
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
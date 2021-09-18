from os import getenv, path

basedir = path.abspath(path.dirname(__file__))

class Config(object):
    # Used for securely signing the session cookie and can be used for other security-related needs
    SECRET_KEY = getenv("SECRET_KEY") or 'you-will-never-guess'
    DB_NAME = getenv("DB_NAME")
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")

    SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL') or \
        'sqlite:///' + path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
from os import getenv

class Config(object):
    # Used for securely signing the session cookie and can be used for other security-related needs
    SECRET_KEY = getenv("SECRET_KEY")
    DB_NAME = getenv("DB_NAME")
    DB_USERNAME = getenv("DB_USERNAME")
    DB_PASSWORD = getenv("DB_PASSWORD")
    DB_HOST = getenv("DB_HOST")
    BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")
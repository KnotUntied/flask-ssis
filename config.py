from os import getenv, path

basedir = path.abspath(path.dirname(__file__))

class Config(object):
    # Used for securely signing the session cookie and can be used for other security-related needs
    SECRET_KEY = getenv("SECRET_KEY") or 'you-will-never-guess'

    BOOTSTRAP_SERVE_LOCAL = getenv("BOOTSTRAP_SERVE_LOCAL")

    MYSQL_HOST = getenv("MYSQL_HOST")
    MYSQL_PORT = int(getenv("MYSQL_PORT"))
    MYSQL_USER = getenv("MYSQL_USER")
    MYSQL_PASSWORD = getenv("MYSQL_PASSWORD")
    MYSQL_DB = getenv("MYSQL_DB")

    CLOUDINARY_NAME = getenv("CLOUDINARY_NAME")
    CLOUDINARY_KEY = getenv("CLOUDINARY_KEY")
    CLOUDINARY_SECRET = getenv("CLOUDINARY_SECRET")

    ITEMS_PER_PAGE = 10

    # max approx 10 MB
    MAX_CONTENT_LENGTH = 1024 * 1024 * 10

    # SQLALCHEMY_DATABASE_URI = getenv('DATABASE_URL') or \
    #     'sqlite:///' + path.join(basedir, 'app.db')
    # SQLALCHEMY_TRACK_MODIFICATIONS = False
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mysqldb import MySQL
# from flask_mysqldb import MySQL
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

import cloudinary

from config import Config

db = MySQL()
# db = SQLAlchemy()
# migrate = Migrate()
bootstrap = Bootstrap()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    # migrate.init_app(app, db)
    bootstrap.init_app(app)

    cloudinary.config(
        cloud_name = app.config['CLOUDINARY_NAME'], 
        api_key = app.config['CLOUDINARY_KEY'], 
        api_secret = app.config['CLOUDINARY_SECRET'],
        secure = True
    )

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    from app.students import bp as students_bp
    app.register_blueprint(students_bp, url_prefix='/students')

    from app.courses import bp as courses_bp
    app.register_blueprint(courses_bp, url_prefix='/courses')

    from app.colleges import bp as colleges_bp
    app.register_blueprint(colleges_bp, url_prefix='/colleges')

    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    return app

from app import models

from flask import Blueprint

bp = Blueprint('colleges', __name__)

from app.colleges import routes
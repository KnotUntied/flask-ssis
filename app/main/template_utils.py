from flask import request
from werkzeug.urls import url_encode

from app.main import bp


@bp.app_template_global()
def modify_query(**new_values):
    args = request.args.copy()

    for key, value in new_values.items():
        args[key] = value

    return '{}?{}'.format(request.path, url_encode(args))
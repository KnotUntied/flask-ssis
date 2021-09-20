from flask import redirect, url_for

from app.main import bp

@bp.route('/index/')
@bp.route('/')
def index():
    return redirect(url_for('students.index'))
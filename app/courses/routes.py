from flask import render_template, flash, redirect, request, url_for, current_app

from app import db
from app.courses import bp
from app.models import Course, College

@bp.route('/index/')
@bp.route('/')
def index():
    return render_template('courses/index.html', title='Courses')
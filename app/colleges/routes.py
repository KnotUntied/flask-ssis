from flask import render_template, flash, redirect, request, url_for, current_app

from app import db
from app.colleges import bp
from app.models import College

@bp.route('/index/')
@bp.route('/')
def index():
    return render_template('colleges/index.html', title='Colleges')

@bp.route('/add/', methods=['GET', 'POST'])
def add():
    return render_template('colleges/index.html', title='Courses')

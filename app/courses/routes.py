from flask import render_template, flash, redirect, request, url_for, current_app, abort
from flask_paginate import Pagination, get_page_parameter

from app import db
from app.courses import bp
from app.courses.forms import AddCourseForm, EditCourseForm, SearchCourseForm
from app.main.forms import EmptyForm
from app.models import Course, College

@bp.route('/index/')
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'code')
    order = request.args.get('order', 'asc')

    code = request.args.get('code') or None
    name = request.args.get('name') or None
    college = request.args.get('college') or None

    paginated = Course.get_paginated(
        page, current_app.config['ITEMS_PER_PAGE'], sort, order,
        code, name, college)

    pagination = Pagination(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        total=Course.count_query(code, name, college),
        bs_version=3)

    form = EmptyForm()
    return render_template(
        'courses/index.html',
        title='Courses',
        courses=paginated,
        pagination=pagination,
        form=form,
        sort=sort,
        order=order)

@bp.route('/add/', methods=['GET', 'POST'])
def add():
    # TODO: Instruct user to create college if no colleges created.
    form = AddCourseForm()
    form.college.choices = College.get_value_label()

    if form.validate_on_submit():
        new = Course()
        form.populate_obj(new)
        new.add()
        flash('{} {} has been added.'.format(form.code.data, form.name.data), 'success')
        return redirect(url_for('courses.index'))
    return render_template('courses/form.html', title='Add Course', form=form)

@bp.route('/profile/<code>/')
def profile(code):
    course = Course.get_one(code) or abort(404)
    college = College.get_one(course.college)

    form = EmptyForm()
    return render_template('courses/profile.html', course=course, college=college, form=form)

@bp.route('/edit/<code>/', methods=['GET', 'POST'])
def edit(code):
    course = Course.get_one(code) or abort(404)
    form = EditCourseForm(obj=course)
    form.college.choices = College.get_value_label()

    if form.validate_on_submit():
        updated = Course()
        form.populate_obj(updated)
        updated.edit(course.code)
        flash('Edit successful.', 'success')
        return redirect(url_for('courses.profile', code=updated.code))
    return render_template('courses/form.html', title='Edit Course', form=form)

@bp.route('/delete/<code>/', methods=['POST'])
def delete(code):
    course = Course.get_one(code)
    Course.delete(code)
    flash('{} {} has been deleted.'.format(course.code, course.name), 'danger')
    return redirect(url_for('courses.index'))

@bp.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchCourseForm()
    form.college.choices = College.get_value_label()

    if form.validate_on_submit():
        return redirect(url_for(
            'courses.index',
            code=form.code.data or None,
            name=form.name.data or None,
            college=form.college.data or None))
    return render_template('courses/form.html', title='Search Course', form=form)
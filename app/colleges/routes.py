from flask import render_template, flash, redirect, request, url_for, current_app, abort
from flask_paginate import Pagination, get_page_parameter

from app import db
from app.colleges import bp
from app.colleges.forms import AddCollegeForm, EditCollegeForm, SearchCollegeForm
from app.main.forms import EmptyForm
from app.models import College

@bp.route('/index/')
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'code')
    order = request.args.get('order', 'asc')

    code = request.args.get('code') or None
    name = request.args.get('name') or None

    paginated = College.get_paginated(
        page, current_app.config['ITEMS_PER_PAGE'], sort, order,
        code, name)

    pagination = Pagination(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        total=College.count_query(code, name),
        bs_version=3)

    form = EmptyForm()
    return render_template(
        'colleges/index.html',
        title='Colleges',
        colleges=paginated,
        pagination=pagination,
        form=form,
        sort=sort,
        order=order)

@bp.route('/add/', methods=['GET', 'POST'])
def add():
    form = AddCollegeForm()

    if form.validate_on_submit():
        new = College()
        form.populate_obj(new)
        new.add()
        flash('{} {} has been added.'.format(form.code.data, form.name.data), 'success')
        return redirect(url_for('colleges.index'))
    return render_template('colleges/form.html', title='Add College', form=form)

@bp.route('/profile/<code>/')
def profile(code):
    college = College.get_one(code) or abort(404)
    form = EmptyForm()
    return render_template('colleges/profile.html', college=college, form=form)

@bp.route('/edit/<code>/', methods=['GET', 'POST'])
def edit(code):
    college = College.get_one(code) or abort(404)
    form = EditCollegeForm(obj=college)

    if form.validate_on_submit():
        updated = College()
        form.populate_obj(updated)
        updated.edit(college.code)
        flash('Edit successful.', 'success')
        return redirect(url_for('colleges.profile', code=updated.code))
    return render_template('colleges/form.html', title='Edit College', form=form)

@bp.route('/delete/<code>/', methods=['POST'])
def delete(code):
    college = College.get_one(code)
    College.delete(code)
    flash('{} {} has been deleted.'.format(college.code, college.name), 'danger')
    return redirect(url_for('colleges.index'))

@bp.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchCollegeForm()

    if form.validate_on_submit():
        return redirect(url_for(
            'colleges.index',
            code=form.code.data or None,
            name=form.name.data or None))
    return render_template('colleges/form.html', title='Search College', form=form)
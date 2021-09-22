from flask import render_template, flash, redirect, request, url_for, current_app
from flask_paginate import Pagination, get_page_parameter

from app import db
from app.students import bp
from app.students.forms import AddStudentForm, EditStudentForm, SearchStudentForm
from app.models import Student, Course

@bp.route('/index/')
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    students = Student.query.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    pagination = Pagination(page=page, per_page=current_app.config['ITEMS_PER_PAGE'], total=Student.query.count(), bs_version=3)
    return render_template(
        'students/index.html',
        title='Students',
        students=students.items,
        pagination=pagination)

@bp.route('/add/', methods=['GET', 'POST'])
def add():
    # TODO: Instruct user to create course if no courses created.
    form = AddStudentForm()

    courses = Course.query.all()
    form.course.choices = list(course.to_choice() for course in courses)

    if form.validate_on_submit():
        student = Student(
            id=form.id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            course=form.course.data,
            year=form.year.data,
            gender=form.gender.data)
        db.session.add(student)
        db.session.commit()
        flash('{} {} {} has been added.'.format(form.id.data, form.firstname.data, form.lastname.data), 'success')
        return redirect(url_for('students.index'))
    return render_template('students/form.html', title='Add Student', form=form)

# Unnecessary as of now, but may be expanded in the future.
@bp.route('/profile/<id>')
def profile(id):
    student = Student.query.filter_by(id=id).first_or_404()
    course = Course.query.get(student.course)
    return render_template('students/profile.html', student=student, course=course)

@bp.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    student = Student.query.get(id)
    form = EditStudentForm()

    courses = Course.query.all()
    form.course.choices = list(course.to_choice() for course in courses)

    if form.validate_on_submit():
        student.id        = form.id.data
        student.firstname = form.firstname.data
        student.lastname  = form.lastname.data
        student.course    = form.course.data
        student.year      = form.year.data
        student.gender    = form.gender.data
        db.session.commit()
        flash('Edit successful.')
        return redirect(url_for('students.view', id=student.id))
    elif request.method == 'GET':
        form.id.data        = student.id
        form.firstname.data = student.firstname
        form.lastname.data  = student.lastname
        if student.course in [choice[0] for choice in form.course.choices]:
            form.course.data = student.course
        # TODO: Instruct user to create course if no courses created.
        elif form.course.choices:
            form.course.data = form.course.choices[0][0]
        print(form.course.data)
        form.year.data      = student.year
        form.gender.data    = student.gender
    return render_template('students/form.html', title='Edit Student', form=form)

@bp.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchStudentForm()

    courses = Course.query.all()
    form.course.choices = list(course.to_choice() for course in courses)

    if form.validate_on_submit():
        return redirect(url_for(
            'students.index',
            id=form.id.data or None,
            firstname=form.firstname.data or None,
            lastname=form.lastname.data or None))
    return render_template('students/search.html', title='Search Student', form=form)
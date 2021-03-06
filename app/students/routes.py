from flask import render_template, flash, redirect, request, url_for, current_app, abort
from flask_paginate import Pagination, get_page_parameter

from cloudinary.uploader import upload as cloudinary_upload, destroy as cloudinary_destroy
from cloudinary.utils import cloudinary_url

from app import db
from app.students import bp
from app.students.forms import AddStudentForm, EditStudentForm, SearchStudentForm
from app.main.forms import EmptyForm
from app.models import Student, Course, College

@bp.route('/index/')
@bp.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'id')
    order = request.args.get('order', 'asc')

    # students = Student.query.order_by(
    #     db.asc(sort) if order == 'asc' else db.desc(sort))

    # id = request.args.get('id')
    # if id:
    #     students = students.filter(Student.id.contains(id))
    # firstname = request.args.get('firstname')
    # if firstname:
    #     students = students.filter(Student.firstname.contains(firstname))
    # lastname = request.args.get('lastname')
    # if lastname:
    #     students = students.filter(Student.lastname.contains(lastname))
    # course = request.args.getlist('course')
    # if course:
    #     students = students.filter(Student.course.in_(course))
    # year = request.args.getlist('year')
    # if year:
    #     students = students.filter(Student.year.in_(year))
    # gender = request.args.getlist('gender')
    # if gender:
    #     students = students.filter(Student.gender.in_(gender))

    id = request.args.get('id') or None
    firstname = request.args.get('firstname') or None
    lastname = request.args.get('lastname') or None
    course = request.args.getlist('course') or None
    year = request.args.getlist('year') or None
    gender = request.args.getlist('gender') or None

    # paginated = students.paginate(page, current_app.config['ITEMS_PER_PAGE'], False)
    paginated = Student.get_paginated(
        page, current_app.config['ITEMS_PER_PAGE'], sort, order,
        id, firstname, lastname, course, year, gender)

    pagination = Pagination(
        page=page,
        per_page=current_app.config['ITEMS_PER_PAGE'],
        total=Student.count_query(id, firstname, lastname, course, year, gender),
        bs_version=3)

    form = EmptyForm()
    return render_template(
        'students/index.html',
        title='Students',
        # students=paginated.items,
        students=paginated,
        pagination=pagination,
        form=form,
        sort=sort,
        order=order,
        cloudinary_url=cloudinary_url)

@bp.route('/add/', methods=['GET', 'POST'])
def add():
    # TODO: Instruct user to create course if no courses created.
    # Querying for choices has to be done in the view
    form = AddStudentForm()
    form.course.choices = Course.get_value_label()

    # courses = Course.query.all()
    # form.course.choices = list(course.to_choice() for course in courses)

    if form.validate_on_submit():
        new = Student()
        form.populate_obj(new)
        if form.photo.data:
            cloudinary_response = cloudinary_upload(form.photo.data, upload_preset='ssis_student', invalidate=True)
            new.avatar = cloudinary_response['public_id']
        new.add()
        # db.session.add(student)
        # db.session.commit()
        flash('{} {} {} has been added.'.format(form.id.data, form.firstname.data, form.lastname.data), 'success')
        return redirect(url_for('students.index'))
    return render_template('students/form.html', title='Add Student', form=form)

# Unnecessary as of now, but may be expanded in the future.
@bp.route('/profile/<id>/')
def profile(id):
    student = Student.get_one(id) or abort(404)
    # student = Student.query.filter_by(id=id).first_or_404()
    course = Course.get_one(student.course)
    # course = Course.query.get(student.course)
    if course:
        college = College.get_one(course.college)
    else:
        college = False

    form = EmptyForm()
    return render_template('students/profile.html', student=student, course=course, college=college,
        form=form, cloudinary_url=cloudinary_url)

@bp.route('/edit/<id>/', methods=['GET', 'POST'])
def edit(id):
    student = Student.get_one(id) or abort(404)
    # student = Student.query.get(id)
    form = EditStudentForm(obj=student)
    form.course.choices = Course.get_value_label()

    # courses = Course.query.all()
    # form.course.choices = list(course.to_choice() for course in courses)

    if form.validate_on_submit():
        updated = Student()
        form.populate_obj(updated)
        if form.clear_photo.data and student.avatar:
            student_avatar = student.avatar
            student.avatar = ''
            cloudinary_response = cloudinary_destroy(student_avatar)
        elif form.photo.data:
            cloudinary_response = cloudinary_upload(form.photo.data, upload_preset='ssis_student', invalidate=True)
            updated.avatar = cloudinary_response['public_id']
        updated.edit(student.id)
        # student.id        = form.id.data
        # student.firstname = form.firstname.data
        # student.lastname  = form.lastname.data
        # student.course    = form.course.data
        # student.year      = form.year.data
        # student.gender    = form.gender.data
        # db.session.commit()
        flash('Edit successful.', 'success')
        return redirect(url_for('students.profile', id=updated.id))
    return render_template('students/form.html', title='Edit Student', student=student,
        form=form, cloudinary_url=cloudinary_url)

# TODO: Retain index args after delete
@bp.route('/delete/<id>/', methods=['POST'])
def delete(id):
    student = Student.get_one(id) or abort(404)
    Student.delete(id)
    if student.avatar:
        cloudinary_response = cloudinary_destroy(student.avatar)
    # student = Student.query.filter_by(id=id).first_or_404()
    flash('{} {} {} has been deleted.'.format(student.id, student.firstname, student.lastname), 'danger')
    return redirect(url_for('students.index'))

@bp.route('/search/', methods=['GET', 'POST'])
def search():
    form = SearchStudentForm()
    form.course.choices = Course.get_value_label()

    # courses = Course.query.all()
    # form.course.choices = list(course.to_choice() for course in courses)

    if form.validate_on_submit():
        return redirect(url_for(
            'students.index',
            id=form.id.data or None,
            firstname=form.firstname.data or None,
            lastname=form.lastname.data or None,
            course=form.course.data or None,
            year=form.year.data or None,
            gender=form.gender.data or None))
    return render_template('students/search.html', title='Search Student', form=form)

# https://github.com/Whale67/Flask-Cloudinary/blob/master/app.py#L40
# @bp.route('/signature', methods=['POST'])
# def signature():
#     values = request.values
#     timestamp = values.get('data[timestamp]')
#     public_id = values.get('data[public_id]')
#     custom_coordinates = values.get('data[custom_coordinates]')
#     api_secret = current_app.config['CLOUDINARY_SECRET']
#     signature = 'callback=https://widget.cloudinary.com/cloudinary_cors.html&custom_coordinates=%s&public_id=%s&timestamp=%s&upload_preset=thka8ije%s' % (custom_coordinates,public_id,timestamp,api_secret)
#     signature2 = signature.encode('utf-8')
#     h = sha1(signature2).hexdigest()
#     return '%s' % (h)
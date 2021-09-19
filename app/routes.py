from flask import render_template, flash, redirect, request, url_for

from app import app, db
from app.forms import AddStudentForm, EditStudentForm
from app.models import Student, Course

@app.route('/')
@app.route('/index/')
@app.route('/students/')
def students():
    students = Student.query.all()
    return render_template('students.html', title='Students', students=students)

@app.route('/students/add/', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
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
        flash('{} {} {} has been added.'.format(form.id.data, form.firstname.data, form.lastname.data))
        return redirect(url_for('students'))
    return render_template('student_form.html', title='Add Student', form=form)

# Redundant as of now, but may be expanded in the future
@app.route('/students/<id>')
def view_student(id):
    student = Student.query.filter_by(id=id).first_or_404()
    return render_template('student_view.html', student=student)

@app.route('/students/<id>/edit', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get(id)
    form = EditStudentForm()
    if form.validate_on_submit():
        student.id        = form.id.data
        student.firstname = form.firstname.data
        student.lastname  = form.lastname.data
        student.course    = form.course.data
        student.year      = form.year.data
        student.gender    = form.gender.data
        db.session.commit()
        flash('Edit successful.')
        return redirect(url_for('view_student', id=student.id))
    elif request.method == 'GET':
        form.id.data        = student.id
        form.firstname.data = student.firstname
        form.lastname.data  = student.lastname
        form.course.data    = student.course
        form.year.data      = student.year
        form.gender.data    = student.gender
    return render_template('student_form.html', title='Edit Student', form=form)

@app.route('/courses/')
def courses():
    return render_template('courses.html', title='Courses')

@app.route('/colleges/')
def colleges():
    return render_template('colleges.html', title='Colleges')

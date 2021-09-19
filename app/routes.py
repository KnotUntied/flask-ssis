from flask import render_template, flash, redirect, url_for

from app import app, db
from app.forms import StudentForm
from app.models import Student, Course

@app.route('/')
@app.route('/index/')
@app.route('/students/')
def students():
    students = Student.query.all()
    return render_template('students.html', title='Students', students=students)

@app.route('/students/add/', methods=['GET', 'POST'])
def add_student():
    form = StudentForm()
    if form.validate_on_submit():
        student = Student(
            id=form.id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            course=form.course.data,
            year=form.year.data,
            gender=form.gender.data)
        print(form.gender.data)
        db.session.add(student)
        db.session.commit()
        flash('{} {} {} has been added.'.format(form.id.data, form.firstname.data, form.lastname.data))
        return redirect(url_for('students'))
    return render_template('student-form.html', title='Add Student', form=form)

@app.route('/courses/')
def courses():
    return render_template('courses.html', title='Courses')

@app.route('/colleges/')
def colleges():
    return render_template('colleges.html', title='Colleges')

from flask import render_template

from app import app
from app.forms import StudentForm

@app.route('/')
@app.route('/index')
@app.route('/students')
def student_form():
    # TODO: Remove placeholder list
    students = [
        {
            'id': '2019-0001',
            'firstname': 'John',
            'lastname': 'Doe',
            'course': 'BSCS',
            'year': 1,
            'gender': 'Male'
        },
        {
            'id': '2020-0002',
            'firstname': 'Jane',
            'lastname': 'Doe',
            'course': 'BSCS',
            'year': 1,
            'gender': 'Male'
        }
    ]
    return render_template('students.html', title='Students', students=students)

@app.route('/student-form')
def students():
    form = StudentForm()
    return render_template('student-form.html', title='Add Student', form=form)

@app.route('/courses')
def courses():
    return render_template('courses.html', title='Courses')

@app.route('/colleges')
def colleges():
    return render_template('colleges.html', title='Colleges')

from flask import render_template

from app import app

@app.route('/')
@app.route('/index')
@app.route('/students')
def students():
    return render_template('students.html')

@app.route('/courses')
def courses():
    return render_template('courses.html')

@app.route('/colleges')
def colleges():
    return render_template('colleges.html')

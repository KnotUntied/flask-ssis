from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import ValidationError, AnyOf, DataRequired, Length, NumberRange, Regexp
from app.models import Student, Course, College

def validate_name(form, field):
    excluded_chars = '1234567890'
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f'Character {char} is not allowed in name.')

class StudentForm(FlaskForm):
    id = StringField(label='ID Number (YYYY-NNNN)', validators=[DataRequired(), Regexp(regex=r'\d{4}\-\d{4}$')])
    firstname = StringField(label='First Name', validators=[DataRequired(), Length(min=1, max=50), validate_name])
    lastname = StringField(label='Last Name', validators=[DataRequired(), Length(min=1, max=50), validate_name])
    course = SelectField(label='Course', validators=[DataRequired()])
    year = IntegerField(label='Year Level', validators=[DataRequired(), NumberRange(min=1, max=4)])
    gender = SelectField(label='Gender',
        choices=['Other', 'Male', 'Female'],
        validators=[
            DataRequired(),
            AnyOf(values=['Other', 'Male', 'Female'])
        ])
    submit = SubmitField(label='Submit')

class AddStudentForm(StudentForm):
    def validate_id(self, id):
        id = Student.query.filter_by(id=id.data).first()
        if id is not None:
            raise ValidationError('ID number has already been used.')

class EditStudentForm(StudentForm):
    def validate_id(self, id):
        new_id = Student.query.filter_by(id=id.data).first()
        if new_id is not None and new_id == id:
            raise ValidationError('ID number has already been used.')


class CourseForm(FlaskForm):
    code = StringField(label='Course Code', validators=[DataRequired(), Length(min=1, max=10)])
    name = StringField(label='Course Name', validators=[DataRequired(), Length(min=1, max=50)])
    college = StringField(label='College', validators=[DataRequired()])
    submit = SubmitField(label='Submit')

class AddCourseForm(CourseForm):
    def validate_code(self, code):
        code = Course.query.filter_by(code=code.data).first()
        if code is not None:
            raise ValidationError('Course code has already been used.')

class EditCourseForm(CourseForm):
    def validate_code(self, code):
        new_code = Course.query.filter_by(code=code.data).first()
        if new_code is not None and new_code == code:
            raise ValidationError('Course code has already been used.')


class CollegeForm(FlaskForm):
    code = StringField(label='College Code', validators=[DataRequired(), Length(min=1, max=5)])
    name = StringField(label='College Name', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField(label='Submit')

class AddCollegeForm(CollegeForm):
    def validate_code(self, code):
        code = College.query.filter_by(code=code.data).first()
        if code is not None:
            raise ValidationError('College code has already been used.')

class EditCollegeForm(CollegeForm):
    def validate_code(self, code):
        new_code = College.query.filter_by(code=code.data).first()
        if new_code is not None and new_code == code:
            raise ValidationError('College code has already been used.')
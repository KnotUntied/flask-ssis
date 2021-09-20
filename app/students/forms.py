from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import ValidationError, AnyOf, DataRequired, Length, NumberRange, Regexp
from app.models import Student


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
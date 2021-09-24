from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import ValidationError, AnyOf, DataRequired, Length, NumberRange, Regexp
from wtforms.widgets import CheckboxInput
from app.models import Student
from app.main.forms import MultiCheckboxField


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
    course = SelectField(
        label='Course',
        validators=[DataRequired()])
    year = IntegerField(label='Year Level', validators=[DataRequired(), NumberRange(min=1, max=4)])
    gender = SelectField(
        label='Gender',
        choices=Student.genders,
        validators=[DataRequired(), AnyOf(values=Student.genders)])
    submit = SubmitField(label='Submit')

class AddStudentForm(StudentForm):
    def validate_id(form, field):
        existing = Student.get_one(field.data)
        # existing = Student.query.filter_by(id=id.data).first()
        if existing:
            raise ValidationError('ID number has already been used.')

class EditStudentForm(StudentForm):
    def validate_id(form, field):
        existing = Student.get_one(field.data)
        # existing = Student.query.filter_by(id=field.data).first()
        if existing and existing.id == field.data:
            raise ValidationError('ID number has already been used.')

class SearchStudentForm(FlaskForm):
    id = StringField(label='ID Number (YYYY-NNNN)', validators=[Regexp(regex=r'[\d\-]*')])
    firstname = StringField(label='First Name', validators=[Length(max=50), validate_name])
    lastname = StringField(label='Last Name', validators=[Length(max=50), validate_name])
    course = SelectMultipleField(label='Course (hold Ctrl or Shift to select multiple)')
    year = MultiCheckboxField(
        label='Year Level',
        # 2-tuples are required for SelectMultipleField, for some reason
        choices=[(y, y) for y in Student.years],
        option_widget=CheckboxInput())
    gender = MultiCheckboxField(
        label='Gender',
        choices=[(g, g) for g in Student.genders],
        option_widget=CheckboxInput())
    submit = SubmitField(label='Submit')
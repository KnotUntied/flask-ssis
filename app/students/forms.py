from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import BooleanField, IntegerField, RadioField, SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import ValidationError, AnyOf, InputRequired, Length, NumberRange, Regexp
from wtforms.widgets import CheckboxInput
from app.models import Student
from app.main.forms import MultiCheckboxField


def validate_name(form, field):
    excluded_chars = '1234567890'
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f'Character {char} is not allowed in name.')

def validate_avatar(form, field):
    pass

class StudentForm(FlaskForm):
    id = StringField(label='ID Number (YYYY-NNNN)', validators=[InputRequired(), Regexp(regex=r'\d{4}\-\d{4}$')])
    firstname = StringField(label='First Name', validators=[InputRequired(), Length(min=1, max=50), validate_name])
    lastname = StringField(label='Last Name', validators=[InputRequired(), Length(min=1, max=50), validate_name])
    course = SelectField(
        label='Course',
        validators=[InputRequired()])
    year = RadioField(
        label='Year Level',
        choices=Student.YEARS,
        validators=[InputRequired(), AnyOf(values=Student.YEARS)])
    gender = RadioField(
        label='Gender',
        choices=Student.GENDERS,
        validators=[InputRequired(), AnyOf(values=Student.GENDERS)])
    # TODO: Validate if cloudinary URL works
    photo = FileField(
        label='Photo (max 10 MB, preferably square) (cancel via file upload dialog to clear)',
        validators=[FileAllowed(['jpg', 'jpeg', 'png'], 'Only PNG or JPG files are allowed.')])

class AddStudentForm(StudentForm):
    def validate_id(form, field):
        existing = Student.get_one(field.data)
        # existing = Student.query.filter_by(id=id.data).first()
        if existing:
            raise ValidationError('ID number has already been used.')

class EditStudentForm(StudentForm):
    clear_photo = BooleanField(label='Remove Photo')
    def validate_id(form, field):
        existing = Student.get_one(field.data)
        # existing = Student.query.filter_by(id=field.data).first()
        if existing and existing.id != field.object_data:
            raise ValidationError('ID number has already been used.')

class SearchStudentForm(FlaskForm):
    id = StringField(label='ID Number (YYYY-NNNN)', validators=[Regexp(regex=r'[\d\-]*')])
    firstname = StringField(label='First Name', validators=[Length(max=50), validate_name])
    lastname = StringField(label='Last Name', validators=[Length(max=50), validate_name])
    course = SelectMultipleField(label='Course (hold Ctrl or Shift to select multiple)')
    year = MultiCheckboxField(
        label='Year Level',
        # 2-tuples are required for SelectMultipleField, for some reason
        choices=[(y, y) for y in Student.YEARS],
        option_widget=CheckboxInput())
    gender = MultiCheckboxField(
        label='Gender',
        choices=[(g, g) for g in Student.GENDERS],
        option_widget=CheckboxInput())
    submit = SubmitField(label='Submit')
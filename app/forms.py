from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, StringField, SubmitField
from wtforms.validators import AnyOf, DataRequired, NumberRange, Regexp

def validate_name(form, field):
    excluded_chars = '1234567890'
    for char in field.data:
        if char in excluded_chars:
            raise ValidationError(
                f'Character {char} is not allowed in name.')

class StudentForm(FlaskForm):
    # idyear = IntegerField(validators=[DataRequired()])
    # idnumber = IntegerField(validators=[DataRequired()])
    id = StringField(label='ID Number (YYYY-NNNN)', validators=[DataRequired(), Regexp(regex=r'\d{4}\-\d{4}$')])
    firstname = StringField(label='First Name', validators=[DataRequired(), validate_name])
    lastname = StringField(label='Last Name', validators=[DataRequired(), validate_name])
    course = SelectField(label='Course',
        choices=['test1', 'test2', 'test3'],
        validators=[
            DataRequired(),
            AnyOf(values=['test1', 'test2', 'test3'])
        ])
    year = IntegerField(label='Year Level', validators=[DataRequired(), NumberRange(min=1, max=4)])
    gender = SelectField(label='Gender',
        choices=['Other', 'Male', 'Female'],
        validators=[
            DataRequired(),
            AnyOf(values=['Other', 'Male', 'Female'])
        ])
    submit = SubmitField(label='Submit')

class CourseForm(FlaskForm):
    code = StringField(label='Course Code', validators=[DataRequired()])
    name = StringField(label='Course Name', validators=[DataRequired()])
    college = StringField(label='College', validators=[DataRequired(), AnyOf(values=['test1', 'test2', 'test3'])])
    submit = SubmitField(label='Submit')

class CollegeForm(FlaskForm):
    code = StringField(label='College Code', validators=[DataRequired()])
    name = StringField(label='College Name', validators=[DataRequired()])
    submit = SubmitField(label='Submit')
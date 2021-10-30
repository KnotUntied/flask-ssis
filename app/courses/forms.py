from flask_wtf import FlaskForm
from wtforms import SelectField, SelectMultipleField, StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from app.models import Course


class CourseForm(FlaskForm):
    code = StringField(label='Course Code', validators=[InputRequired(), Length(min=1, max=10)])
    name = StringField(label='Course Name', validators=[InputRequired(), Length(min=1, max=50)])
    college = SelectField(label='College', validators=[InputRequired()])
    submit = SubmitField(label='Submit')

class AddCourseForm(CourseForm):
    def validate_code(form, field):
        existing = Course.get_one(field.data)
        if existing:
            raise ValidationError('Course code has already been used.')

class EditCourseForm(CourseForm):
    def validate_code(form, field):
        existing = Course.get_one(field.data)
        if existing and existing.code != field.object_data:
            raise ValidationError('Course code has already been used.')

class SearchCourseForm(FlaskForm):
    code = StringField(label='Course Code', validators=[Length(max=10)])
    name = StringField(label='Course Name', validators=[Length(max=50)])
    college = SelectMultipleField(label='College (hold Ctrl or Shift to select multiple)')
    submit = SubmitField(label='Submit')
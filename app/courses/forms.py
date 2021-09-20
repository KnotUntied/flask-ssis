from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import Course


class CourseForm(FlaskForm):
    code = StringField(label='Course Code', validators=[DataRequired(), Length(min=1, max=10)])
    name = StringField(label='Course Name', validators=[DataRequired(), Length(min=1, max=50)])
    college = SelectField(label='College', validators=[DataRequired()])
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
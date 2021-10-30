from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, InputRequired, Length
from app.models import College


class CollegeForm(FlaskForm):
    code = StringField(label='College Code', validators=[InputRequired(), Length(min=1, max=5)])
    name = StringField(label='College Name', validators=[InputRequired(), Length(min=1, max=50)])
    submit = SubmitField(label='Submit')

class AddCollegeForm(CollegeForm):
    def validate_code(form, field):
        existing = College.get_one(field.data)
        if existing:
            raise ValidationError('College code has already been used.')

class EditCollegeForm(CollegeForm):
    def validate_code(form, field):
        existing = College.get_one(field.data)
        if existing and existing.code != field.object_data:
            raise ValidationError('College code has already been used.')

class SearchCollegeForm(FlaskForm):
    code = StringField(label='College Code', validators=[Length(max=5)])
    name = StringField(label='College Name', validators=[Length(max=50)])
    submit = SubmitField(label='Submit')
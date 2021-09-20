from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Length
from app.models import College


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
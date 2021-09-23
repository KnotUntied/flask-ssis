from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, SubmitField
from wtforms.widgets import CheckboxInput, ListWidget


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()
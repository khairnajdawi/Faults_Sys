from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,  DateTimeField,TextAreaField,TimeField
from wtforms.validators import DataRequired, AnyOf, URL

class AddBrancheForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )

class EditBrancheForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    is_active = SelectField(
        'is_active',
        validators=[DataRequired()],
        choices=[('True','Yes'),('False','No')]
    )
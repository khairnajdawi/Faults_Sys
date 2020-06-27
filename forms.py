from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField,  DateTimeField,TextAreaField,TimeField
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, AnyOf, URL
from models import ITSections

class AddBranchForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )

class EditBranchForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    is_active = SelectField(
        'is_active',
        validators=[DataRequired()],
        choices=[('True','Yes'),('False','No')]
    )

class AddITSectionForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )

class EditITSectionForm(FlaskForm):
    name = StringField(
        'name',
        validators=[DataRequired()]
    )
    is_active = SelectField(
        'is_active',
        validators=[DataRequired()],
        choices=[('True','Yes'),('False','No')]
    )


class AddFaultTypeForm(FlaskForm):
    fault_type = StringField(
        'fault_type',
        validators=[DataRequired()]
    )   
    it_section = SelectField(
        'it_section',
        validators=[DataRequired()]
    )
    def __init__(self, *args, **kwargs): 
        super(AddFaultTypeForm, self).__init__(*args, **kwargs)
        self.it_section.choices = [(s.id, s.name) for s in ITSections.query.filter_by(is_active=True).all()]



class EditFaultTypeForm(FlaskForm):
    fault_type = StringField(
        'fault_type',
        validators=[DataRequired()]
    )   
    it_section = SelectField(
        'it_section',
        validators=[DataRequired()]
    )
    def __init__(self, *args, **kwargs): 
        super(EditFaultTypeForm, self).__init__(*args, **kwargs)
        self.it_section.choices = [(s.id, s.name) for s in ITSections.query.filter_by(is_active=True).all()]

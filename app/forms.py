from flask_appbuilder.forms import DynamicForm, DateTimeField, DateTimePickerWidget

from wtforms import SelectField, StringField, IntegerField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms.widgets import TextArea

class ContactForm(DynamicForm):
    name = StringField('Full name')
    email = StringField('Email',validators=[Optional(),Email(), Length(min=6, max=40)])

    current_ds = SelectField('Is your organization currently data-driven?', choices=[('',''),('yes','Yes'),('no','No')])
    sector = SelectField("Sector",choices=[('',''),('academia','academia'),('public','public'),
                                           ('private','private'),('press','press'),('other','other')])
    company = StringField("Company/gov't agency")
    position = SelectField("Position", choices=[('',''),('CEO','CEO'),('vice-president','vice-president'),
                                                ('senior-management','senior-management'),
                                                ('mid-level management','mid-level management'),
                                                ('non-management','non-management'),
                                                ('Data scientist','data scientist'),
                                                ('other','other')])

    phone = StringField('Contact number',validators=[Optional(), NumberRange(min=8, max=14)])
    intend_ds = IntegerField('How long (in months) before your organization intends to become data-driven?',
                             validators=[Optional()])
    current_bi_tool = StringField('Which BI tool does your organization currently use?', default="None")
    contact_you = SelectField('Would you like us to contact you?',choices=[('',''),('yes','Yes'),('no','No')])
    #contact_timestamp = DateTimeField('If you would like us to contact you please select a date and time',
                                      #widget=DateTimePickerWidget())
    pain_points = TextAreaField('If you have pain points for us to discuss please list them (separated by a comma)')
    interest_in_conference = SelectField("Are you interested in attending the conference?",
                                         choices=[('', ''), ('yes', 'Yes'), ('no', 'No')])

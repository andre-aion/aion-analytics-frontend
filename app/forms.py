from flask_appbuilder.forms import DynamicForm, DateTimeField, DateTimePickerWidget
from flask_mongoengine.wtf import model_form
from mongoengine import ReferenceField

from wtforms import SelectField, StringField, IntegerField, TextAreaField, FloatField, FieldList
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange
from wtforms.widgets import TextArea
from app import dbmongo
from app.models import Employee, ProjectType, Project, Risk


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


# ------------  PROJECT
class EmployeeForm(DynamicForm):
    name = StringField('Name')
    gender = SelectField('Gender',choices=[('male','male'),('female','female')])
    hourly_rate = FloatField('Hourly rate($)')
    department = StringField('Department')
    title = StringField('Title')
    dob = DateTimeField('Date of Birth',widget=DateTimePickerWidget())

def employees():
    lst = []
    for employee in Employee.objects:
        lst.append(employee.name)
    return lst

def project_type():
    lst = []
    for item in ProjectType.objects:
        lst.append(item.type)
    return lst

def project():
    lst = []
    for item in Project.objects:
        if item.status == 'open':
            lst.append(item.name)
    return lst

class ProjectForm(DynamicForm):
    name = StringField('Project name')
    type = SelectField('ProjectType',choices=[(i, i) for i in project_type()])
    manager = SelectField('Manager',choices=[(e, e) for e in employees()])
    manager_gender = SelectField('Gender',choices=[('male','male'),('female','female')])
    manager_age = IntegerField("Manager's age")
    startdate_proposed = DateTimeField('Actual start date',widget=DateTimePickerWidget())
    enddate_proposed = DateTimeField('Actual start date',widget=DateTimePickerWidget())
    startdate_actual = DateTimeField('Actual start date',widget=DateTimePickerWidget())
    enddate_actual = DateTimeField('Actual start date',widget=DateTimePickerWidget())
    status = SelectField('Project status',choices = [('open', 'open'), ('closed', 'closed')])

class ProjectTaskForm(DynamicForm):
    project = SelectField('Project',choices=[(e, e) for e in project()])
    employee = SelectField('Manager',choices=[(e, e) for e in employees()])
    start = DateTimeField('Task start date',widget=DateTimePickerWidget())
    end = DateTimeField('Task start date',widget=DateTimePickerWidget())


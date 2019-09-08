from datetime import datetime

import bson
from flask_appbuilder.forms import DynamicForm, DateTimeField, DateTimePickerWidget
from flask_mongoengine.wtf import model_form
from mongoengine import ReferenceField, DateField, IntField

from wtforms import SelectField, StringField, IntegerField, TextAreaField, FloatField, FieldList
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
from wtforms.widgets import TextArea
from app import dbmongo
from app.models import Employee, ProjectType, Project, Risk, ElectionEvent, AppointmentWorkDays, AppointmentHolidays, \
    AppointmentEmployeeUnAvailability

DATEFORMAT = "%Y-%m-%d %H:%M:%S"
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
########################################################
########## ELECTIONS ENDED ###########################


class ElectionEventForm(DynamicForm):
    type = SelectField('Type',choices=[('rally','rally'),('lime','lime')])
    name = StringField()
    location = StringField()
    venue_type = StringField()
    city = StringField()
    timestamp_started_actual = DateTimeField('Actual Start datetime',widget=DateTimePickerWidget())
    timestamp_started_proposed = DateTimeField('Proposed Start datetime',widget=DateTimePickerWidget())
    timestamp_ended = DateTimeField()
    artists_performed = StringField('Who performed')
    food = StringField('Meal provided')

class ElectionEventAttendeeForm(DynamicForm):
    event = StringField()
    name = StringField()

    gender = SelectField('Gender',choices=[('male','male'),('female','female'),('other','other')])
    dob = DateTimeField('Date of Birth',widget=DateTimePickerWidget())

    city_of_residence = SelectField('In which city do you live?',
                                     choices=[('Trincity','Trincity'),('Arima','Arima')])
    role = SelectField('What is your role today?',
                       choices=[('headline','headliner'),('attendee','attendee'),
                                ('volunteer','volunteer')])

    job = StringField()
    twitter = StringField()
    instagram = StringField()
    facebook = StringField()
    email = StringField()
    phone_number = StringField()
    interests = StringField()
    concerns = StringField()
    most_interesting_topics_today = StringField()

    voting_for = SelectField('Who do you intend to vote for',
                             choices=[('PNM','PNM'),('UNC','UNC'),('NAR','NAR'),('Other','Other')])


    want_to_volunteer = SelectField('Do you want to volunteer',
                                    choices=[('yes','Yes'),('No','No'),('Other','Other')])
    event_discovery = SelectField('How did you find out about this event',
                                  choices=[('Friend','Friend'),('Family','Family'),
                                           ('Radio','Radio'),('TV','TV')])
    rate_event = SelectField('Please rate the event',choices=[(1,1),(2,2),(3,3),(4,4),(5,5)])
    #events_attended = IntField()


########################################################
########## ELECTIONS ENDED ###########################

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

'''
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

'''


# --------------------  CUSTOM VALIDATORS ----------------------------------

def get_parent_date(id,type='milestone',datetype='startdate'):
    if type == 'milestone':
        object = Project.objects.get(id=bson.objectid.ObjectId(id))
        print('LINE 91:',object)
        if object is not None:
            if datetype == 'startdate':
                if object.startdate_proposed is not None:
                    tmp_date = object.startdate_proposed
            elif datetype == 'enddate':
                if object.enddate_proposed is not None:
                    tmp_date = object.enddate_proposed
            if tmp_date is not None:
                if isinstance(tmp_date,str):
                    return datetime.strptime(object.startdate_proposed,DATEFORMAT)
                return tmp_date
        return None


class StartDateValidate(object):
    def __init__(self, enddate,type='project', message=None):
        self.enddate = enddate
        self.DATEFORMAT = "%Y-%m-%d %H:%M:%S"
        arr = enddate.split('_')
        self.period = arr[-1]
        if not message:
            message = 'startdate_{} cannot be less than {}'.format(arr[-1],enddate)
        self.message = message
        self.type = type


    def __call__(self, form, field):
        if field.data is not None and self.enddate is not None:
            mydate = form[self.enddate].data
            print(mydate)
            if isinstance(mydate,str):
                mydate = datetime.strptime(mydate,self.DATEFORMAT)
            if field.data >= mydate:
                raise ValidationError(self.message)

        # ensure startdate is not less than parent date
        if self.type in ['milestone','task']:
            print('VALIDATING PARENT DATES')
            parent = 'milestone'
            if self.type == 'milestone':
                parent = 'project'

            id = form[parent].data.id
            print('ID:',id)
            for item in ['startdate','enddate']:
                parent_date = get_parent_date(id, self.type,datetype=item)
                if item == 'startdate':
                    if parent_date > field.data:
                        message = '{} proposed startdate cannot preceed proposed {} startdate'.format(self.type,parent)
                        raise ValidationError(message)
                elif item == 'enddate':
                    if self.period != 'actual':
                        if parent_date < field.data and self:
                            message = '{} proposed startdate cannot exceed proposed {} enddate'.format(self.type, parent)

                            raise ValidationError(message)





# --------------------------------------------------------------------------


# ------------------------------  VALIDATOR, AVAILABILITY ------------
class AvailabilityValidate(object):
    def __init__(self,available,message=None):
        if not available:
            message = 'Sorry that date or time is unavailable, please try another date/date and time'
        self.message = message

    def available(self, form, field):
        try:
            days = AppointmentWorkDays.objects()
            allow_booking = True
            workdays = []
            if not form.data.override:
                if days is not None and len(days) > 0:
                    for item in days:
                        workdays.append(item.day.lower())
                else:
                     workdays = ['monday','tuesday','wednesday','thursday','friday']

                if field.data.strftime["%A"] not in workdays:
                    allow_booking = False

                # ensure that is not on a holiday
                holidays = AppointmentHolidays.objects('date'==field.data.date())
                if holidays is not None and len(holidays) > 0:
                    allow_booking = False
                else:
                    unavailibilty = AppointmentEmployeeUnAvailability.objects(
                                                                              'start' <= field.data,
                                                                              'end' >= field.data)
                    if unavailibilty is not None and len(unavailibilty) > 0:
                        allow_booking = False

            return allow_booking

        except:
            return False
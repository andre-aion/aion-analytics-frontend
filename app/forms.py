from datetime import datetime

import bson
from flask_appbuilder.forms import DynamicForm, DateTimeField, DateTimePickerWidget
from flask_login import current_user
from flask_mongoengine.wtf import model_form
from mongoengine import ReferenceField, DateField, IntField, BooleanField

from wtforms import SelectField, StringField, IntegerField, TextAreaField, FloatField, FieldList
from wtforms.validators import DataRequired, Email, Length, Optional, NumberRange, ValidationError
from wtforms.widgets import TextArea
from app import dbmongo, db, app
from app.models import Employee, ProjectType, Project, Risk, ElectionEvent, AppointmentWorkDays, \
    AppointmentUnavailability, AppointmentProcedure, AppointmentClient, AppointmentHoliday

import MySQLdb
import pandas as pd
from flask import session, g



connection = MySQLdb.connect(user='admin',password='password',
                             database='aion_analytics',host='127.0.0.1')

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

rate_choices = []

for i in range(0,101):
    rate_choices.append((str(i),str(i)))

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
    rate_event = SelectField('Please rate the event',choices=rate_choices)
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

def all_doctors():
    lst = []
    sql = "select first_name, last_name from ab_user"
    df = pd.read_sql(sql,connection)
    if df is not None and len(df) > 0:

        df['name'] = df.apply(lambda x: x['first_name'] + ' '+x['last_name'],axis=1)
        lst = list(df.name.unique())
    return lst

@app.before_request
def before_request():
    print(current_user)



def logged_in_doctor():
    before_request()
    is_a_doctor = False
    if current_user is not None:
        lst = all_doctors()
        sql = """select abu.id, first_name, last_name from ab_user abu
        inner join ab_user_role abur on abu.id = abur.user_id
        inner join ab_role abr on abur.role_id = abr.id 
        where abr.name = 'appointment_doctor' """
        df = pd.read_sql(sql,connection)
        if df is not None and len(df) > 0:
            df['name'] = df.apply(lambda x: x['first_name'] + ' ' + x['last_name'], axis=1)
            df = df[df['name'] == current_user]
            if df is not None and len(df) > 0:
                print(df)
                ids = list(df['id'].unique())[0]
                print(ids)
        else:
            return None

        return current_user
    return 'not a doctor'

class AppointmentBookingForm(DynamicForm):
    doctor = SelectField('doctor',choices=[(i, i) for i in all_doctors()])
    timestamp = DateTimeField('Requested time',widget=DateTimePickerWidget())
    procedure = StringField()
    customer = StringField()
    override = BooleanField(default=False)  # overide workdays or holidays or schedule
    available = StringField(default=False)


class DoctorAvailabilityValidate(object):
    def __init__(self,doctor,message=None):
        self.message = message
        self.doctor = doctor

    def __call__(self, form, field):
        try:
            # self.doctor is doctor name
            days = AppointmentWorkDays.objects.get()
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
                holidays = AppointmentHoliday.objects.get('date' == field.data.date())
                if holidays is not None and len(holidays) > 0:
                    allow_booking = False
                else:
                    unavailabilty = AppointmentUnavailability\
                        .objects.get('start' <= field.data,'end' >= field.data,
                                     'doctor' == self.doctor)
                    if unavailabilty is not None and len(unavailabilty) > 0:
                        allow_booking = False

            return allow_booking
        except:
            return False



class AppointmentUnavailabilityForm(DynamicForm):
    __tablename__ = 'appointment_unavailability'
    doctor = StringField('Logged in',default=logged_in_doctor())
    start = DateTimeField('Start',widget=DateTimePickerWidget())
    end = DateTimeField('End',widget=DateTimePickerWidget())
    reason = StringField()


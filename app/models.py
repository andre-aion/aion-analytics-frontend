from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import AuditMixin
from mongoengine import Document, DateField, DictField
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, FloatField, IntField,BooleanField

from app import dbmongo

"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""
class ToolEventName(Model):
    id = Column(Integer,primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)

    def __repr__(self):
        return self.name

class ToolClassification(Model):
    id = Column(Integer,primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)

    def __repr__(self):
        return self.name

class Tool(Model):
    id = Column(Integer,primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)

    def __repr__(self):
        return self.name

class ToolHasClassification(Model):
    id = Column(Integer,primary_key=True)
    tool = Column(String, ForeignKey('tool.id'))
    tool_ = relationship("Tool")
    classification = Column(String, ForeignKey('tool_classification.id'))
    classification_ = relationship("ToolClassification")


"""
assoc_tool_classification = Table('tool_has_classification',Model.metadata,
                                  Column('id',Integer,primary_key=True),
                                  Column('tool_id', Integer, ForeignKey('tool.id')),
                                  Column('classification_id', Integer, ForeignKey('tool_classification.id')))
                                  """

class ToolEvent(Model):
    id = Column(Integer,primary_key=True)
    tool = Column(Integer,ForeignKey('tool.id'))
    tool_ = relationship("Tool")
    event = Column(Integer,ForeignKey('tool_event_name.id'))
    event_ = relationship("ToolEventName")
    timestamp = Column(Date)

    def toolname(self):
        return self.tool_.name

    def eventname(self):
        return self.event_.name


class ContactInfo(Model): # carry out surveys
    __tablename__ = 'contact_info'
    id = Column(Integer,primary_key=True)
    name = Column(String)
    company = Column(String)
    position = Column(String)
    sector = Column(String)
    email = Column(String)
    phone = Column(String)
    current_ds = Column(String)
    intend_ds = Column(Integer)
    current_bi_tool = Column(String)
    contact_you = Column(String)
    interest_in_conference = Column(String)
    pain_points = Column(String)

    def __repr__(self):
        return self.name


class Glossary(Model):
    __tablename__ = 'glossary'
    id = Column(Integer,primary_key=True)
    term = Column(String(100), unique=True, nullable=False)
    description = Column(String)
    note = Column(String)


# /////////////////////////////////// MYSQL VIEWS
class ToolEventAll(Model):
    __tablename__ = 'view_tool_events'
    id = Column(Integer,primary_key=True)
    tool = Column(String)
    event = Column(String)
    timestamp = Column(Date)
    classification = Column(String)


# ################################# MONGO DB
class ProjectType(Document):
    __tablename__ = ' project_type'
    type = StringField(required=True)
    description = StringField(max_length=200)

    def __repr__(self):
        return self.type

    # return selected attribute in dropddowns
    def __str__(self):
        return self.type


class Employee(Document):
    __tablename__ = 'employee'
    name = StringField(required=True,max_length=50, unique=True)
    gender = StringField()
    hourly_rate = FloatField()
    department = StringField()
    title = StringField()
    dob = DateTimeField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name


class Project(Document):
    __tablename__ = 'project'
    name = StringField(max_length=60, required=True)
    type = ReferenceField(ProjectType,required=True)
    owner = ReferenceField(Employee, required=True)
    startdate_proposed = DateTimeField(required=True)
    enddate_proposed = DateTimeField(required=True)
    startdate_actual = DateTimeField()
    enddate_actual = DateTimeField()
    description = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return """{}: {} - {}""".format(self.name, self.startdate_proposed.date(), self.enddate_proposed.date())

    def start(self):
        return self.startdate_proposed

    def end(self):
        return self.enddate_proposed


class ProjectMilestone(Document):
    __tablename__ = 'project_milestone'
    name = StringField(max_length=60, required=True, unique=True)
    project = ReferenceField(Project, required=True)
    owner = ReferenceField(Employee, required=True)
    key_delivery = StringField(max_length=100)
    startdate_proposed = DateTimeField(required=True)
    enddate_proposed = DateTimeField(required=True)
    startdate_actual = DateTimeField()
    enddate_actual = DateTimeField()
    notes = StringField(max_length=1000)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return """{}: {} - {}""".format(self.name, self.startdate_proposed.date(), self.enddate_proposed.date())

    def startdate(self):
        return self.startdate_proposed


class ProjectTask(Document):
    __tablename__ = 'project_task'
    name = StringField(max_length=60, required=True)
    milestone = ReferenceField(ProjectMilestone, required=True)
    owner = ReferenceField(Employee, required=True)
    key_delivery = StringField(max_length=100)
    type = ReferenceField(ProjectType, required=True)
    startdate_proposed = DateTimeField(required=True)
    enddate_proposed = DateTimeField(required=True)
    startdate_actual = DateTimeField()
    enddate_actual = DateTimeField()
    value_proposed = FloatField()
    value_delivered = FloatField()
    notes = StringField(max_length=1000)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name


class ProjectStatuses(Document):
    __tablename__ = 'project_statuses'
    status = StringField(required=True,unique=True)

    def __unicode__(self):
        return self.status

    def __repr__(self):
        return self.status

    # return selected attribute in dropddowns
    def __str__(self):
        return self.status


class ProjectStatus(Document):
    __tablename__ = 'project_status'
    project = ReferenceField(Project,required=True)
    status = ReferenceField(ProjectStatuses,required=True)
    timestamp = DateTimeField(required=True)
    desc = StringField(max_length=500)

    def __unicode__(self):
        return self.status

    def __repr__(self):
        return self.status

    # return selected attribute in dropddowns
    def __str__(self):
        return self.project+': ' + self.status

class ProjectDeliveryMetric(Document):
    metric = StringField(max_length=60, required=True,unique=True)
    type = StringField()
    desc = StringField(max_length=500)

class ProjectDelivery(Document):
    __tablename__ = 'project_delivery'
    name = StringField(max_length=60, required=True)
    task = ReferenceField(ProjectTask,required=True)
    metric = ReferenceField(ProjectDeliveryMetric,required=True)
    unit = StringField(max_length=60,required=True)
    target = FloatField(required=True)
    target_date = DateTimeField(required=True)
    desc = StringField(max_length=500)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name

class ProjectDeliveryTracker(Document):
    __tablename__ = 'project_delivery_tracker'
    delivery = ReferenceField(ProjectDelivery,required=True)
    stat = FloatField(required=True)
    timestamp = DateTimeField(required=True)
    desc = StringField(max_length=500)

    def __unicode__(self):
        return self.stat

    def __repr__(self):
        return self.stat

    # return selected attribute in dropddowns
    def __str__(self):
        return self.stat


class ProjectDeliveryRating(Document):
    __tablename__ = 'project_rating'
    delivery = ReferenceField(ProjectDelivery, required=True)
    timestamp = DateField()
    rating = FloatField(min_value=0,max_value=100)
    analyst = ReferenceField(Employee, required=True)
    note = StringField(max_length=500)

# -------  RISK ---------------------


class RiskMatrix(Document):
    __tablename__= 'risk_matrix'
    name = StringField(required=True,unique=True)
    project = ReferenceField(Project, required=True)
    analysis_date = DateTimeField()
    analyst = ReferenceField(Employee, required=True)
    desc =    StringField(max_length=500)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name

class RiskLikelihood(Document):
    __tablename__ = 'risk_likelihood'
    level = StringField(max_length=20)
    value = IntField()
    desc = StringField(max_length=300)

    def __unicode__(self):
        return self.level

    def __repr__(self):
        return self.level

    # return selected attribute in dropddowns

    def __str__(self):
        return self.level

class RiskSeverity(Document):
    __tablename__ = 'risk_severity'
    level = StringField(max_length=20)
    value = IntField()
    desc = StringField(max_length=300)

    def __unicode__(self):
        return self.level

    def __repr__(self):
        return self.level

    # return selected attribute in dropddowns

    def __str__(self):
        return self.level

class RiskCategory(Document):
    __tablename__ = 'risk_category'
    name = StringField(max_length=50)
    desc = StringField(max_length=500)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name


class Risk(Document):
    __tablename__ = 'risk'
    matrix = ReferenceField(RiskMatrix, required=True)
    risk = StringField(required=True,max_length=200,unique=True)
    category = ReferenceField(RiskCategory, required=True)
    desc = StringField(max_length=500)
    created_at = DateTimeField()


    def __unicode__(self):
        return self.risk

    def __repr__(self):
        return self.risk

        # return selected attribute in dropddowns

    def __str__(self):
        return self.risk

class RiskAnalysis(Document):
    __tablename__ = 'risk_analysis'
    risk = ReferenceField(Risk, required=True)
    likelihood = ReferenceField(RiskLikelihood, required=True)
    likelihood_comment = StringField(max_length=200)
    severity = ReferenceField(RiskSeverity, required=True)
    severity_comment = StringField(max_length=200)

class RiskSolution(Document):
    __tablename__ = 'risk_solution'
    project = ReferenceField(Project, required=True)
    solution = StringField(max_length=500,unique=True)
    suggestion_date = DateTimeField()
    success_rating = IntField(min_value=1,max_value=100)
    desc = StringField(max_length=500)

# -------------- ETL -------------------
class EtlScheduler(Document):
    __tablename__ = 'etl_scheduler'
    job = StringField(required=True,unique=True)
    run_hour = IntField(min_value=0,max_value=23,required=True)
    run_minute = IntField(min_value=0,max_value=59,required=True)
    reset_flag = StringField()
    reset_startdate = DateTimeField()
    reset_enddate = DateTimeField()


# -------------- ETL -------------------
class Etl(Document):
    __tablename__ = 'etl'
    etl = StringField(required=True)

    def __unicode__(self):
        return self.etl

    def __repr__(self):
        return self.etl

        # return selected attribute in dropddowns

    def __str__(self):
        return self.etl

class EtlParameterType(Document):
    __tablename__ = 'etl_parameter_type'
    type = StringField(required=True)

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

        # return selected attribute in dropddowns

    def __str__(self):
        return self.type

class EtlParameter(Document):
    __tablename__ = 'etl_parameter'
    #twitter = ListField(StringField(),default=lambda:['expressupdates'])
    etl = ReferenceField(Etl, required=True)
    type = ReferenceField(EtlParameterType, required=True)
    label = StringField(required=True)
    handle = StringField(required=True)
    startdate = DateField()

# --------------------- CONSORTIUM -------------------------

class Gender(Document):
    __tablename__ = 'gender'
    gender = StringField()
    def __unicode__(self):
        return self.gender

    def __repr__(self):
        return self.gender

    def __str__(self):
        return self.gender


class BusinessType(Document):
    __tablename__ = 'business_type'
    type = StringField(required=True)
    desc = StringField()

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    # return selected attribute in dropddowns

    def __str__(self):
        return self.type

class BusinessEventType(Document):
    __tablename__ = 'business_event_type'
    type = StringField(required=True)
    desc = StringField()
    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type



class Business(Document):
    __tablename__ = 'business'
    name = StringField(required=True,unique=True)
    type = ReferenceField(BusinessType,required=True)
    desc = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class EducationLevel(Document):
    __tablename__ = 'education_level'
    level = StringField()

    def __unicode__(self):
        return self.level

    def __repr__(self):
        return self.level

    def __str__(self):
        return self.level


class BusinessStaff(Document):
    __tablename__ = 'business_staff'
    name = StringField(required=True,unique=True)
    gender = ReferenceField(Gender)
    dob = DateField()
    highest_ed = ReferenceField(EducationLevel)
    city = StringField()
    position = StringField()
    job_title = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class Like(Document):
    __tablename__ = 'like'
    name = StringField(required=True, unique=True)
    desc = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class BusinessEvent(Document):
    __tablename__ = 'business_event'
    name = StringField(required=True)
    start_proposed = DateTimeField()
    end_proposed = DateTimeField()
    start_actual = DateTimeField()
    end_actual = DateTimeField()
    manager = ReferenceField(BusinessStaff)
    type = ReferenceField(BusinessEventType, required=True)
    business = ReferenceField(Business, required=True)
    desc = StringField()
    rate = FloatField()
    rate_period = StringField()


    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class BusinessEventStaff(Document):
    __tablename__ = 'business_event_staff'
    event = ReferenceField(BusinessEvent)
    staff = ReferenceField(BusinessStaff,unique=True)


class BusinessDiscoveryMethod(Document):
    __tablename__ = 'business_event_discovery_method'

    method = StringField()

    def __unicode__(self):
        return self.method

    def __repr__(self):
        return self.method

    def __str__(self):
        return self.method

class BusinessEventDiscover(Document):
    __tablename__ = 'business_event_discover'
    event = ReferenceField(BusinessEvent)
    method = ReferenceField(BusinessDiscoveryMethod)
    discovery_timestamp = DateTimeField()



class BusinessPatron(Document):
    __tablename__ = 'business_patron'
    name = StringField()
    dob = DateField()
    gender = ReferenceField(Gender)
    address1 = StringField()
    address2 = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    phone_number_mobile = StringField()
    phone_number_office = StringField()
    phone_number_home = StringField()
    twitter = StringField()
    facebook = StringField()
    instagram = StringField()
    email = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name



class BusinessPatronLike(Document):
    __tablename__ = 'business_patron_like'
    patron = ReferenceField(BusinessPatron,required=True)
    like = ReferenceField(Like,required=True)
    desc = StringField()

class BusinessPatronNetwork(Document):
    patron1 = ReferenceField(BusinessPatron,required=True)
    patron2 = ReferenceField(BusinessPatron,required=True)
    relationship = StringField()
    discovery_method = StringField()
    timestamp = DateTimeField()


class BusinessEventPatronStatuses(Document):
    __tablename__ = 'business_event_patron_status'
    status = StringField(required=True)
    desc = StringField()

    def __unicode__(self):
        return self.status

    def __repr__(self):
        return self.status

    def __str__(self):
        return self.status



class BusinessEventPatronStatus(Document):
    __tablename__ = 'business_event_patron'
    event = ReferenceField(BusinessEvent,required=True)
    patron = ReferenceField(BusinessPatron,required=True)
    status = ReferenceField(BusinessEventPatronStatuses,required=True)
    timestamp = DateTimeField()
    notes = StringField()


class BusinessEventRating(Document):
    __tablename__ = 'business_event_rating'
    event = ReferenceField(BusinessEvent, required=True)
    timestamp = DateTimeField()
    rating = IntField(min_value=1,max_value=100)
    desc = StringField(max_length=500)
    

# ---------------------- MEETINGS -------------------------- #

class MeetingType(Document):
    __tablename__ = 'meeting_type'
    type = StringField(required=True)
    desc = StringField()

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    # return selected attribute in dropddowns
    def __str__(self):
        return self.type


class Meeting(Document):
    __tablename__ = 'meeting'
    name = StringField(required=True)
    topic = StringField(required=True)
    start_proposed = DateTimeField()
    end_proposed = DateTimeField()
    start_actual = DateTimeField()
    end_actual = DateTimeField()
    owner = ReferenceField(Employee)
    type = ReferenceField(MeetingType, required=True)
    project = ReferenceField(Project, required=True)
    desc = StringField()
    rate = FloatField()
    rate_period = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class MeetingAttendee(Document):
    __tablename__ = 'meeting_attendee'
    meeting = ReferenceField(Meeting)
    name = StringField(required=True,unique=True)
    gender = ReferenceField(Gender)
    dob = DateField()
    highest_ed = ReferenceField(EducationLevel)
    location = StringField()
    position = StringField()
    prep_time = FloatField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

############### -------------------------  CRUISING CLUB
class BCCCountry(Document):
    __tablename__ = 'bcc_country'
    country = StringField(required=True,max_length=60)


class BCCMembershipType(Document):
    __tablename__ = 'bcc_membership_type'
    type = StringField(max_length=30)
    description = StringField(max_length=500)

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type


class BCCHobby(Document):
    __tablename__ = 'bcc_hobby'
    hobby = StringField()
    def __unicode__(self):
        return self.hobby

    def __repr__(self):
        return self.hobby

    def __str__(self):
        return self.hobby


class BCCReasonJoin(Document):
    __tablename__ = 'bcc_reason_join'
    reason = StringField()
    def __unicode__(self):
        return self.reason

    def __repr__(self):
        return self.reason

    def __str__(self):
        return self.reason

class BCCPerson(Document):
    __tablename__ = 'bcc_person'
    name = StringField(required=True,unique=True)
    gender = ReferenceField(Gender)
    dob = DateField()
    highest_ed = ReferenceField(EducationLevel)
    job_title = StringField()
    place_of_employment = StringField()
    referrer = StringField()
    address_1 = StringField(required=True)
    address_2 = StringField()
    city = StringField(required=True)
    state = StringField()
    parish = StringField()
    country = StringField(required=True,default='Barbados')
    postal_code = StringField()


    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class BCCPersonHobbies(Document):
    __tablename__ = 'bcc_person_hobbies'
    person = ReferenceField(BCCPerson)
    hobby = ReferenceField(BCCHobby)

class BCCDuesList(Document):
    __tablename__ = 'bcc_dues_list'
    month = StringField(required=True)
    amount = FloatField(required=True)


class BCCRegistration(Document):
    __tablename__ = 'bcc_dues_list'
    timestamp = DateTimeField()
    type = ReferenceField(BCCMembershipType)
    person = ReferenceField(BCCPerson)
    registration_no = StringField(max_length=8)


class BCCPersonReasonJoin(Document):
    __tablename__ = 'bcc_reason_join'
    person = ReferenceField(BCCPerson)
    reason = ReferenceField(BCCReasonJoin)


class BCCActivity(Document):
    __tablename__ = 'bcc_activity'

    activity = StringField()
    
    def __unicode__(self):
        return self.activity

    def __repr__(self):
        return self.activity

    def __str__(self):
        return self.activity


class BCCVisit(Document):
    __tablename__ = 'bcc_visit'
    person = ReferenceField()
    arrived = DateTimeField()
    departed = DateTimeField()

    def __unicode__(self):
        return self.person

    def __repr__(self):
        return self.person

    def __str__(self):
        return self.person



class BCCVisitActivity(Document):
    __tablename__ = 'bcc_visit_activity'
    visit = ReferenceField(BCCPerson)
    activity = ReferenceField(BCCActivity)
    
    

class BCCVisitNetwork(Document):
    __tablename__ = 'bcc_visit_network'
    visitor = ReferenceField(BCCVisit)
    friend = ReferenceField(BCCPerson)


class BCCBarItems(Document):
    __tablename__ = 'bcc_bar_items'
    item = StringField(max_length=40,required=True)
    price = FloatField(required=True)

    def __unicode__(self):
        return self.item

    def __repr__(self):
        return self.item

    def __str__(self):
        return self.item


class BCCTab(Document):
    __tablename__ = 'bcc_tab'
    visitor = ReferenceField(BCCVisit,Required=True)
    item = ReferenceField(Required=True)
    amount = IntField(required=True,default=1)
    timestamp = DateTimeField(required=True)
    




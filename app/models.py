import datetime

from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from mongoengine import Document, DateField, DictField, DynamicDocument
from mongoengine import DateTimeField, StringField, ReferenceField, \
    FloatField, IntField,BooleanField,ListField
from flask_login import current_user
import random
import string


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))
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

def Time_Now():
    return datetime.datetime.utcnow()


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
    name = StringField(required=True)
    member_number = StringField(required=True,unique=True)
    gender = ReferenceField(Gender)
    dob = DateField()
    highest_ed = ReferenceField(EducationLevel)
    job_title = StringField()
    place_of_employment = StringField()
    referrer = StringField()
    phone_no = StringField(max_length=10)
    email = StringField(max_length=30)
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
        return """{}-{} """.format(self.name,self.member_number)
    

class BCCStatus(Document):
    __tablename__ = 'bcc_person_status'
    status = StringField(required=True)
    
    def __unicode__(self):
        return self.status

    def __repr__(self):
        return self.status

    def __str__(self):
        return self.status


class BCCPersonStatus(Document):
    __tablename__ = 'bcc_person_status'
    person = ReferenceField(BCCPerson,required=True)
    status = ReferenceField(BCCStatus,required=True)
    timestamp = DateTimeField()


class BCCPersonHobby(Document):
    __tablename__ = 'bcc_person_hobby'
    person = ReferenceField(BCCPerson)
    hobby = ReferenceField(BCCHobby)


class BCCDuesList(Document):
    __tablename__ = 'bcc_dues_list'
    month = StringField(required=True)
    amount = FloatField(required=True)

    def __unicode__(self):
        return self.month

    def __repr__(self):
        return self.month

    def __str__(self):
        return self.month



class BCCVesselType(Document):
    __tablename__ = 'bcc_vessel_type'
    type = StringField(required=True)
    
    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type



class BCCVesselSize(Document):
    __tablename__ = 'bcc_vessel_size'
    size = StringField(required=True)
    
    def __unicode__(self):
        return self.size

    def __repr__(self):
        return self.size

    def __str__(self):
        return self.size



class BCCVesselTypeSizePrice(Document):
    __tablename__ = 'bcc_vessel_size_price'
    type = ReferenceField(BCCVesselType,required=True)
    size = ReferenceField(BCCVesselSize,required=True)
    fee = FloatField(required=True)
 
    

class BCCVessel(Document):
    __tablename__ = 'bcc_vessel'
    person = ReferenceField(BCCPerson)
    registration_no = StringField(max_length=8)
    type = ReferenceField(BCCVesselType)
    length = FloatField()
    width = FloatField()
    color = StringField()



class BCCRegistration(Document):
    __tablename__ = 'bcc_registration'
    membership_type = ReferenceField(BCCMembershipType)
    person = ReferenceField(BCCPerson)
    vessel_info = ReferenceField(BCCVesselType)
    vessel_price_storage = ReferenceField(BCCVesselTypeSizePrice)
    timestamp = DateTimeField()



class BCCRelationshipType(Document):
    __tablename__ = 'bcc_relationship_type'
    relationship = StringField(required=True)

    def __unicode__(self):
        return self.relationship

    def __repr__(self):
        return self.relationship

    def __str__(self):
        return self.relationship


class BCCRelationship(Document):
    __tablename__ = 'bcc_relationship'
    person = ReferenceField(BCCRegistration)
    relationship = ReferenceField(BCCRelationshipType)



class BCCPersonReasonJoin(Document):
    __tablename__ = 'bcc_person_reason_join'
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
    person = ReferenceField(BCCPerson)
    arrived = DateTimeField(required=True,default=datetime.datetime.now())
    departed = DateTimeField()


    def __unicode__(self):
        return self.person

    def __repr__(self):
        return self.person

    def __str__(self):
        tmp = self.departed
        if tmp is None:
            tmp == "Still here..."
        return """{}:{}-{}""".format(self.person,self.arrived,tmp)

class BCCVisitActivity(Document):
    __tablename__ = 'bcc_visit_activity'
    visit = ReferenceField(BCCPerson)
    activity = ReferenceField(BCCActivity)
    start = DateTimeField(required=True,default=datetime.datetime.now())
    end = DateTimeField()


class BCCVisitNetwork(Document):
    __tablename__ = 'bcc_visit_network'
    visitor = ReferenceField(BCCVisit)
    friend = ReferenceField(BCCPerson)


class BCCArea(Document):
    __tablename__ = 'bcc_area'
    area = StringField(required=True)
    description = StringField(max_length=150)

    def __unicode__(self):
        return self.area

    def __repr__(self):
        return self.area

    def __str__(self):
        return self.area


class BCCItemCategory(Document):
    __tablename__ = 'bcc_item_categories'
    category = StringField(max_length=40,required=True)
    area = ReferenceField(BCCArea,required=True)
    description = StringField(max_length=150)

    def __unicode__(self):
        return self.category

    def __repr__(self):
        return self.category

    def __str__(self):
        return self.category


class BCCBarItem(Document):
    __tablename__ = 'bcc_bar_items'
    item = StringField(max_length=40,required=True)
    category = ReferenceField(BCCItemCategory, required=True)
    price = FloatField(required=True,default=0.0)

    def __unicode__(self):
        return self.item

    def __repr__(self):
        return self.item

    def __str__(self):
        return """{}-price = ${}""".format(self.item,self.price)


class BCCBarVisitTab(DynamicDocument):
    __tablename__ = 'bcc_bar_tab'
    tab = StringField(required=True,default=randomString(10))
    visit = ReferenceField(BCCVisit,Required=True)
    opened_at = DateTimeField(required=True,default=Time_Now())

    def amount(self):
        # Put your query here
        # return len(db.session.query(Result).filter(id_person == self.id).all())
        amount = 0
        try:
            tab_purchases = BCCBarVisitTabPurchase.objects('tab'==self.tab)
            if tab_purchases:
                for purchase in tab_purchases:
                    amount += purchase.amount
            print("SET BY CURRENT TAB")
            return '${}'.format(amount)
        except:
            print('TAB CALCULATION EXCETPTION')
            return '$0.00'



    def __unicode__(self):
        return self.tab

    def __repr__(self):
        return self.tab

    def __str__(self):
        return """{}:{}""".format(self.tab,self.opened_at)


class BCCBarVisitTabPurchase(Document):
    __tablename__ = 'bcc_visit_purchase'
    tab = ReferenceField(BCCBarVisitTab,Required=True)
    item = ReferenceField(BCCBarItem, Required=True)
    amount = IntField(required=True,default=1)
    timestamp = DateTimeField(required=True,default=Time_Now())

    def total(self):
        total = 0
        items = BCCBarItem.objects('_id' == self.item)
        print('_________',items)
        for item in items:
            if item is not None:
                total = item.price * self.amount

        return """${}""".format(round(total, 2))

    def __unicode__(self):
        return self.item

    def __repr__(self):
        return self.item

    def __str__(self):
        return """{} {}(s)={}""".format(self.amount, self.item,self.total())


class BCCBarVisitTabPayment(DynamicDocument):
    __tablename__ = 'bcc_tab_payment'
    tab = ReferenceField(BCCBarVisitTab,Required=True)
    payment = FloatField(Required=True,default=0)
    timestamp = DateTimeField(Required=True,default=Time_Now())

    def amount(self):
        # Put your query here
        # return len(db.session.query(Result).filter(id_person == self.id).all())
        amount = 0
        try:
            tab_purchases = BCCBarVisitTabPurchase.objects('tab' == self.tab)
            if tab_purchases:
                for purchase in tab_purchases:
                    amount += purchase.amount
            print("SET BY CURRENT TAB")
            return '${}'.format(amount)
        except:
            print('TAB CALCULATION EXCEPTION')
            return '$0.00'

#  #### RENTAL

class BCCVisitRentalItem(Document):
    __tablename__ = 'bcc_rental_items'
    item = StringField(max_length=40,required=True)
    category = ReferenceField(BCCItemCategory, required=True)
    price = FloatField(required=True,default=0.0)
    period = StringField(max_length=40,required=True)
    serial_no = StringField(required=True,max_length=40)

    def __unicode__(self):
        return self.item

    def __repr__(self):
        return self.item

    def __str__(self):
        return """{}-price = ${}""".format(self.item,self.price)


class BCCVisitRental(Document):
    __tablename__ = 'bcc_visit_rental'
    visit = ReferenceField(BCCVisit,Required=True)
    item = ReferenceField(BCCVisitRentalItem,Required=True)
    timestamp_taken = DateTimeField(Required=True)
    timestamp_to_be_returned = DateTimeField(Required=True)
    timestamp_returned = DateTimeField()

    def __unicode__(self):
        return self.item

    def __repr__(self):
        return self.item

    def __str__(self):
        return """{}: taken @ {} - returned @ {}""".format(self.item, self.timestamp_taken, self.timestamp_returned)

# ###########################################################
########### ELECTIONS ##############################

class ElectionEvent(Document):
    __tablename__ = 'election_event'
    name = StringField(Required=True)
    type = StringField()
    location = StringField(Required=True)
    venue_type = StringField()
    city = StringField(Required=True)
    timestamp_started_actual = DateTimeField(Required=True)
    timestamp_ended = DateTimeField(Required=True)
    timestamp_started_proposed = DateTimeField()
    artists_performed = StringField(max_length=400)
    food = StringField(max_length=400)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return """{}: held @ {} - start @ {}""".format(self.name, self.location,self.timestamp_started_actual)


class ElectionEventAttendees(Document):
    __tablename__ = 'election_event_attendees'
    event = StringField()
    name = StringField(required=True)
    gender = StringField()
    dob = DateField()

    city_of_residence = StringField()
    role = StringField()

    job = StringField()
    twitter = StringField()
    instagram = StringField()
    facebook = StringField()
    email = StringField()
    phone_number = StringField()
    interests = StringField(max_length=400)
    concerns = StringField(max_length=400)
    most_interesting_topics_today = StringField(max_length=200)
    voting_for = StringField()

    want_to_volunteer = StringField()
    event_discovery = StringField()
    rate_event = StringField()
    #events_attended = IntField()


    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return """{} attended {}""".format(self.name, self.event)


#  #######################################################
#########################################################

###############      MEDICAL  ############################

###########  INVENTORY MGMT ###########
class InventoryProductType(Document):
    __tablename__ = 'inventory_product_type'
    type = StringField(required=True)

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type

class InventoryProduct(Document):
    __tablename__ = 'inventory_product'
    name = StringField(required=True)
    type = ReferenceField(InventoryProductType,required=True)
    product_number = StringField()
    container = StringField()
    size = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return """{} - {}""".format(self.name, self.product_number)


class InventoryProductCost(Document):
    __tablename__ = 'inventory_product_unitcost'
    product = ReferenceField(InventoryProduct,required=True)
    timestamp = DateTimeField(required=True)
    cost = FloatField()

    def __unicode__(self):
        return self.cost

    def __repr__(self):
        return self.cost

    def __str__(self):
        return """{} : ${}""".format(self.product, self.cost)


class InventoryContact(Document):
    __tablename__ = 'inventory_contact'
    name = StringField()
    dob = DateField()
    gender = StringField()
    educational_level = StringField()
    phone_number1 = StringField()
    phone_number2 = StringField()
    email = StringField()
    facebook = StringField()
    company = StringField()
    position = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class InventorySupplier(Document):
    __tablename__ = 'inventory_supplier'
    name = StringField()
    address = StringField()
    city = StringField()
    contact = ReferenceField(InventoryContact)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class InventoryOrder(Document):
    __tablename__ = 'inventory_order'
    product = ReferenceField(InventoryProduct)
    product_cost = ReferenceField(InventoryProductCost)
    timestamp_ordered = DateTimeField()
    amount_ordered = FloatField()
    supplier = ReferenceField(InventorySupplier)
    when_expected = DateTimeField()
    when_delivered = DateTimeField()
    delivered_by = ReferenceField(InventoryContact)
    amount_delivered = FloatField()

    def __str__(self):
        return """{} ordered @ {} = ${}""".format(self.product,
                                                  self.timestamp_ordered,self.cost)


class InventoryUsage(Document):
    __tablename__ = 'inventory_stock'
    product = ReferenceField(InventoryProduct)
    timestamp = DateTimeField(required=True,default=Time_Now())
    used_by = ReferenceField(InventoryContact)
    amount_used = DateTimeField(required=True,default=Time_Now())
    
    def __str__(self):
        return """{} {}(s) used""".format(self.amount_used, self.product)


# #####################  APPOINTMENTS #########################

class AppointmentProcedure(Document):
    __tablename__ = 'appointment_type'
    name = StringField(required=True)
    length_in_minutes = IntField(required=True)
    desc = StringField(max_length=300)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class AppointmentProcedureCost(Document):
    __tablename__ = 'appointment_type'
    procedure = ReferenceField(AppointmentProcedure, required=True)
    cost = FloatField(required=True)
    date = DateField()

    def __str__(self):
        return """{} - {} @ {}(s)""".format(self.procedure,
                                            self.cost,self.date)

class AppointmentProcedureItemsUsed(Document):
    __tablename__ = 'appointment_type'
    procedure = ReferenceField(AppointmentProcedure,required=True)
    product = ReferenceField(InventoryProduct,required=True)
    amount = FloatField(max_length=300)

    def __str__(self):
        return """{} - {} {}(s)""".format(self.procedure,self.amount,self.product)



class AppointmentClient(Document):
    __tablename__ = 'appointment_client'
    name = StringField(required=True)
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
    email = StringField(required=True)


    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class AppointmentClientStatus(Document):
    __tablename__ = 'appointment_contact_status'
    name = ReferenceField(AppointmentClient)
    status = StringField(required=True)


    def __str__(self):
        return """{} - {}""".format(self.person,self.status)
    
    
class AppointmentWorkDays(Document):
    __tablename__ = 'appointment_days'
    day = StringField(required=True,unique=True)

    def __unicode__(self):
        return self.day

    def __repr__(self):
        return self.day

    def __str__(self):
        return self.day


class AppointmentWorkHours(DynamicDocument):
    __tablename__ = 'appointment_hours'
    hour = IntField(required=True,unique=True)

    def __unicode__(self):
        return self.hour


    def __repr__(self):
        return self.hour


    def __str__(self):
        return self.hour


class AppointmentHoliday(Document):
    __tablename__ = 'appointment_holiday'
    holiday = StringField(required=True,unique=True)
    date = DateField(required=True)
    reason = StringField()

    def __unicode__(self):
        return self.holiday


    def __repr__(self):
        return self.holiday


    def __str__(self):
        return """{}:{}""".format(self.holiday, self.date)




class AppointmentUnavailability(Document):
    __tablename__ = 'appointment_unavailability'
    doctor = StringField()
    start = DateTimeField()
    end = DateTimeField()
    reason = StringField()


    def __str__(self):
        return """{}- {}:{}""".format(self.doctor, self.start,self.end)


class AppointmentBooking(Document):
    __tablename__ = 'appointment_booking'
    doctor = StringField(required=True)
    timestamp = DateTimeField(required=True)
    procedure = ReferenceField(AppointmentProcedure,required=True)
    customer = ReferenceField(AppointmentClient,required=True)
    override = BooleanField(default=False) # overide workdays or holidays or schedule
    available = BooleanField(default=False)


    def __str__(self):
        return """{},{} @ {} - {}""".format(self.customer,self.procedure,
                                            self.timestamp,self.doctor)



# #########################################################
################# SALES ##############

class SalesIndustryType(Document):
    __tablename__ = 'sales_industry_type'
    type = StringField(required=True)

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type


class SalesIndustrySectorType(Document):
    __tablename__ = 'sales_industry_sector_type'
    type = StringField(required=True)

    def __unicode__(self):
        return self.type

    def __repr__(self):
        return self.type

    def __str__(self):
        return self.type



class SalesCompany(Document):
    __tablename__ = 'sales_company'
    name = StringField(required=True, unique=True)
    type = ReferenceField(BusinessType, required=True)
    address = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    phone_number1 = StringField()
    phone_number2 = StringField()
    Fax = StringField()
    desc = StringField()
    size = IntField()
    financial_ranking = FloatField()
    twitter = StringField()
    instagram = StringField()
    facebook = StringField()
    email = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name

class SalesContact(Document):
    __tablename__ = 'sales_contact'
    name = StringField()
    dob = DateField()
    gender = StringField()
    educational_level = StringField()
    phone_office = StringField()
    phone_mobile = StringField()
    email = StringField()
    facebook = StringField()
    linkedin = StringField()
    company = ReferenceField(SalesCompany)
    title = StringField()
    address = StringField()
    city = StringField()
    state = StringField()
    country = StringField()
    zip_code = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class SalesContactUniversity(Document):
    __tablename__ = 'sales_contact_uni'
    contact = ReferenceField(SalesContact)
    university = StringField()

class SalesContactAffiliations(Document):
    __tablename__ = 'sales_contact_affiliations'
    contact = ReferenceField(SalesContact)
    affiliation = StringField()
    position = StringField()

class SalesContactDonations(Document):
    __tablename__ = 'sales_contact_donations'
    contact = ReferenceField(SalesContact)
    entity = StringField()
    amount = FloatField()

class SalesContactBoardservice(Document):
    __tablename__ = 'sales_contact_boardservice'
    contact = ReferenceField(SalesContact)
    entity = StringField()
    amount = FloatField()
    start = DateField()
    end = DateField()


class SalesCallTracker(Document):
    __tablename__ = 'sales_call_tracker'
    contact = ReferenceField(SalesContact)




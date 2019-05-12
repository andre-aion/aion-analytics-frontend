from flask_appbuilder import Model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date
from sqlalchemy.orm import relationship
from flask_appbuilder.models.mixins import AuditMixin
from mongoengine import Document, DateField
from mongoengine import DateTimeField, StringField, ReferenceField, ListField, FloatField, IntField
from wtforms import SelectField

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

class Project(Document):
    __tablename__ = 'project'
    name = StringField(max_length=60, required=True, unique=True)
    type = dbmongo.ReferenceField(ProjectType)
    manager = StringField()
    key_delivery = StringField(max_length=100)
    startdate_proposed = DateTimeField()
    enddate_proposed = DateTimeField()
    startdate_actual = DateTimeField()
    enddate_actual = DateTimeField()
    status = StringField()

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name


class Employee(Document):
    __tablename__ = 'employee'
    name = StringField(required=True,max_length=50)
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


class ProjectMilestone(Document):
    __tablename__ = 'project_milestone'
    name = StringField(max_length=60, required=True, unique=True)
    project = StringField()
    owner = StringField()
    key_delivery = StringField(max_length=100)
    startdate_proposed = DateTimeField()
    enddate_proposed = DateTimeField()
    startdate_actual = DateTimeField()
    enddate_actual = DateTimeField()
    notes = StringField(max_length=1000)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return self.name

    # return selected attribute in dropddowns
    def __str__(self):
        return self.name


class ProjectTask(Document):
    __tablename__ = 'project_task'
    name = StringField(max_length=60, required=True, unique=True)
    milestone = StringField()
    owner = StringField()
    key_delivery = StringField(max_length=100)
    startdate_proposed = DateTimeField()
    enddate_proposed = DateTimeField()
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


class ProjectRating(Document):
    __tablename__ = 'project_rating'
    project = ReferenceField(Project, required=True)
    timestamp = DateField()
    rating = IntField(min_value=1,max_value=100)
    analyst = ReferenceField(Employee, required=True)
    note = StringField(max_length=500)

# -------  RISK ---------------------

class RiskMatrix(Document):
    __tablename__= 'risk_matrix'
    name = StringField(required=True)
    project = StringField()
    analysis_date = DateTimeField()
    analyst = StringField()
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
    risk = StringField(required=True,max_length=200)
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
    risk = ReferenceField(Risk, required=True)
    solution = StringField(max_length=500)
    suggestion_date = DateTimeField()
    success_rating = IntField(min_value=1,max_value=100)
    desc = StringField(max_length=500)






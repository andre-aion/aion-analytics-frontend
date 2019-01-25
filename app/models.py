from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
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

    def __repr__(self):
        self.output = self.tool_.name + ',' + self.classification_.name
        return self.output

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
    timestamp = Column(DateTime)


    def __repr__(self):
        return self.event
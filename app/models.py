from flask_appbuilder import Model
from flask_appbuilder.models.mixins import AuditMixin, FileColumn, ImageColumn
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship
"""

You can use the extra Flask-AppBuilder fields and Mixin's

AuditMixin will add automatic timestamp of created and modified by who


"""

class Tool_event_name(Model):
    id = Column(Integer,primary_key=True)
    name = Column(String, unique=True)
    desc = Column(String)

    def __repr__(self):
        return self.name

class Tool_event(Model):
    id = Column(Integer,primary_key=True)
    tool = Column(Integer)
    event = Column(Integer)
    timestamp = Column(DateTime)

    def __repr__(self):
        return self.name
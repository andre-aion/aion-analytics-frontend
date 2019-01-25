from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models import ToolEvent, Tool, ToolClassification, ToolHasClassification, ToolEventName
from flask_appbuilder import AppBuilder, expose, BaseView, has_access,ModelView


class ToolEventView(ModelView):
    datamodel = SQLAInterface(ToolEvent)
    list_columns = ['tool_.name','event_.name']
    search_columns = ['timestamp']
    related_views = [Tool,ToolEventName]

class ToolEventNameView(ModelView):
    datamodel = SQLAInterface(ToolEventName)
    search_columns = ['name']
    list_columns = ['name','desc']

class ToolView(ModelView):
    datamodel = SQLAInterface(Tool)
    search_columns = ['name']
    list_columns = ['name','desc']

class ToolClassificationView(ModelView):
    datamodel = SQLAInterface(ToolClassification)
    search_columns = ['name']
    list_columns = ['name','desc']

class ToolHasClassificationView(ModelView):
    datamodel = SQLAInterface(ToolHasClassification)
    list_columns = ['tool_.name','classification_.name']



class DatascienceView(BaseView):
    route_base = 'datascience'

    @expose('/rf_tree')
    def rf_tree(self):
        return self.ender_template('rf_tree.html')

appbuilder.add_link('Rf_tree',
                    href='/datascience/rf_tree',
                    icon='fa-tree',
                    category='Datascience')

appbuilder.add_view(ToolEventView,
                    'Tool events',
                    icon="fa-edit",
                    category='Tools'
                    )
appbuilder.add_view(ToolEventNameView,
                    'events',
                    icon="fa-calendar",
                    category='Tools'
                    )

appbuilder.add_view(ToolClassificationView,
                    'classification',
                    icon="fa-folder",
                    category='Tools'
                    )

appbuilder.add_view(ToolHasClassificationView,
                    'tool classification',
                    icon="fa-folder",
                    category='Tools'
                    )

appbuilder.add_view(ToolView,
                    'tool',
                    icon="fa-wrench",
                    category='Tools'
                    )
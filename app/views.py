from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models import Tool_event, Tool_event_name
from flask_appbuilder import AppBuilder, expose, BaseView, has_access,ModelView

"""
    Create your Views::


    class MyModelView(ModelView):
        datamodel = SQLAInterface(MyModel)


    Next, register your Views::


    appbuilder.add_view(MyModelView, "My View", icon="fa-folder-open-o", category="My Category", category_icon='fa-envelope')
"""

"""
    Application wide 404 error handler
"""

class Tool_eventView(ModelView):
    datamodel = SQLAInterface(Tool_event)
    list_columns = ['tool','event']
    search_columns = ['timestamp']

class Tool_event_nameView(ModelView):
    datamodel = SQLAInterface(Tool_event_name)
    search_columns = ['name']
    list_columns = ['name','desc']

class DatascienceView(BaseView):
    route_base = 'datascience'
    related_views = [Tool_event_name]

    @expose('/rf_tree')
    def rf_tree(self):
        return self.ender_template('rf_tree.html')

appbuilder.add_link('Rf_tree',
                    href='/datascience/rf_tree',
                    icon='fa-tree',
                    category='Datascience')
appbuilder.add_view(Tool_eventView,
                    'Show events',
                    icon="fa-edit",
                    category='View_tool_events_name'
                    )
appbuilder.add_view(Tool_event_nameView,
                    'Show events names',
                    icon="fa-calendar",
                    category='View_tool_events'
                    )


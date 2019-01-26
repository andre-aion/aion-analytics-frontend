from bokeh.client import pull_session
from bokeh.util.session_id import generate_session_id
from flask import render_template, Flask, url_for
from flask_appbuilder.filemanager import ImageManager
from flask_appbuilder.models.sqla.interface import SQLAInterface
from app import appbuilder, db
from app.models import ToolEvent, Tool, ToolClassification, ToolHasClassification, ToolEventName
from flask_appbuilder import expose, BaseView, has_access,ModelView
from config import basedir

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

'''
class Rf_treeView(BaseView):
    default_view = 'rf_tree'
    @expose('/rf_tree')
    def rf_tree(self):
        # im = ImageManager()
        src='/static/img/tier1_tree.png'
        return render_template('rf_tree.html', base_template=appbuilder.base_template,
                               data=src,appbuilder=appbuilder)

'''
class DatascienceView(BaseView):
    default_view = 'analytics'

    @expose('/analytics')
    @has_access
    def analytics(self):
        # pull a new session from a running Bokeh server
        bokeh_server_url = 'http://localhost:5006'
        #bokeh_session = pull_session(url=bokeh_server_url)
        bokeh_session = generate_session_id()
        script = "{}?bokeh-session-id={}".format(bokeh_server_url, bokeh_session)
        return render_template('analytics_index.html', data=script,
                               base_template=appbuilder.base_template,
                               appbuilder=appbuilder)

    @expose('/rf_tree')
    def rf_tree(self):
        # im = ImageManager()
        src = '/static/img/tier1_tree.png'
        return render_template('rf_tree.html', base_template=appbuilder.base_template,
                               data=src, appbuilder=appbuilder)

# #####################################
#          ADD VIEWS

appbuilder.add_view(DatascienceView,
                    'Analytics',
                    icon='fa-line-chart',
                    category='Datascience')


appbuilder.add_link('e.g. Churn decision tree',
                    href='/static/img/tier1_tree.png',
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
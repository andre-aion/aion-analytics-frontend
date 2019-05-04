
from bokeh.util.session_id import generate_session_id
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface

from flask_appbuilder.widgets import ListBlock
from wtforms import SelectField

from app import appbuilder, db
from app.forms import ContactForm
from app.models import ToolEvent, Tool, ToolClassification, \
    ToolHasClassification, ToolEventName, ToolEventAll, ContactInfo, Glossary, Project, Employee, \
    ProjectType, ProjectTask
from flask_appbuilder import expose, BaseView, has_access, ModelView, action, CompactCRUDMixin
from flask_appbuilder.charts.views import DirectByChartView, ChartView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg
from flask_appbuilder.fieldwidgets import DateTimePickerWidget, Select2Widget
from flask_appbuilder.forms import DateTimeField


# MYSQL VIEWS
class ToolEventView(ModelView):
    datamodel = SQLAInterface(ToolEvent)
    list_columns = ['tool_.name','event_.name','timestamp']
    search_columns = ['timestamp']
    related_views = [Tool,ToolEventName]

# MYSQL TABLES
class ToolEventAllView(ModelView):
    datamodel = SQLAInterface(ToolEventAll)
    list_columns = ['tool','event','classification','timestamp']
    search_columns = ['timestamp']

class ToolEventNameView(ModelView):
    datamodel = SQLAInterface(ToolEventName)
    search_columns = ['name']
    list_columns = ['name','desc']

class ToolView(ModelView):
    datamodel = SQLAInterface(Tool)
    search_columns = ['name']
    list_columns = ['name','desc']

@action("muldelete", "Delete", "Delete all Really?", "fa-rocket", single=False)
class ToolClassificationView(ModelView):
    datamodel = SQLAInterface(ToolClassification)
    search_columns = ['name']
    list_columns = ['name','desc']

class ToolHasClassificationView(ModelView):
    datamodel = SQLAInterface(ToolHasClassification)
    list_columns = ['tool_.name','classification_.name']

class ContactInfoView(ModelView):
    datamodel = SQLAInterface(ContactInfo)
    '''
    label_columns = {
        'name':'Full name',
        'company':"Company/gov't agency",
        'email':'Email',
        'phone':'Contact number',
        'current_ds':'Is your organization currently data-driven?',
        'intend_ds':'How long (months) before your organization intend to become data-driven?',
        'current_bi_tool':'What BI tool does your organization currently use?',
        'contact_you':'Would you like us to contact you?',
        'contact_timestamp':'If you would like us to contact you please select a date and time that works for you',
        'pain_points':"If you have pain points for us to discuss please list them, separated by a comma",
        'interest_in_conference':"Are you interested in attending the conference?"
        }
    '''
    list_columns = ['sector']
    search_columns = ['sector']
    add_form = ContactForm

class GlossaryView(ModelView):
    datamodel = SQLAInterface(Glossary)
    list_columns = ['term','description','note']

class DatascienceView(BaseView):
    default_view = 'analytics'
    @expose('/analytics')
    @has_access
    def analytics(self):
        # pull a new session from a running Bokeh server
        bokeh_server_url = 'http://amdatt.ml:5006'
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


# ################### MONGO MODELS ####
class ProjectView(ModelView):
    datamodel = MongoEngineInterface(Project)
    list_columns = ['name','status','startdate_proposed','enddate_proposed','startdate_actual','enddate_actual']


class EmployeeView(ModelView):
    datamodel = MongoEngineInterface(Employee)
    list_columns = ['name','gender','title','hourly_rate']


class ProjectTaskView(ModelView):
    datamodel = MongoEngineInterface(ProjectTask)
    list_columns = ['project','employee','start','end']


class ProjectTypeView(ModelView):
    datamodel = MongoEngineInterface(ProjectType)

# #####################################
#          ADD CHARTS
def pretty_month_year(value):
    return str(value.year)

class EventChartGroupbyView(GroupByChartView):
    datamodel = SQLAInterface(ToolEventAll)
    chart_title = 'Tool events'
    definitions = [
        {
            'label': 'Events',
            'group': 'event',
            'series': [(aggregate_count,'event')]
        },
        {
            'label': 'class',
            'group': 'classification',
            'series': [(aggregate_count, 'classification')]
        },

    ]

class EventChartView(ChartView):
    datamodel = SQLAInterface(ToolEventAll)
    chart_title = 'Tool events'
    search_columns = ['tool','timestamp']
    label_columns = ToolEventAllView.label_columns
    group_by_columns = ['classification','event']



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

appbuilder.add_view(ToolEventAllView,
                    'Tool events info',
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

appbuilder.add_view(ContactInfoView,
                    'Contact info',
                    icon='fa-address-card-o',
                    category='Contacts')

appbuilder.add_view(GlossaryView,
                    'Glossary',
                    icon='fa-book',
                    category='Glossary')

# MONGO VIEWS
appbuilder.add_view(ProjectView,
                    'Projects',
                    icon='fa-industry',
                    category='Projects')

appbuilder.add_view(EmployeeView,
                    'Workers',
                    icon='fa-users',
                    category='Projects')

appbuilder.add_view(ProjectTaskView,
                    'Tasks',
                    icon='fa-tasks',
                    category='Projects')

appbuilder.add_view(ProjectTypeView,
                    'Type',
                    icon='fa-folder',
                    category='Projects')


#   CHART VIEWS
appbuilder.add_view(EventChartView,
                    "Event charts",
                    icon="fa-dashboard",
                    category="Statistics")
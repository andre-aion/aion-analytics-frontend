from flask import g
from bokeh.util.session_id import generate_session_id
from flask import render_template
from flask_appbuilder.fields import QuerySelectField
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder.models.mongoengine.interface import MongoEngineInterface

from flask_appbuilder.widgets import ListBlock
from mongoengine import ValidationError
from wtforms import SelectField
from wtforms.validators import EqualTo

from app import appbuilder, db, dbmongo
from app.forms import ContactForm, EmployeeForm, StartDateValidate
from app.models import ToolEvent, Tool, ToolClassification, \
    ToolHasClassification, ToolEventName, ToolEventAll, ContactInfo, Glossary, Project, Employee, \
    ProjectType, ProjectTask, RiskMatrix, RiskLikelihood, RiskSeverity, Risk, RiskSolution, RiskCategory, RiskAnalysis, \
    ProjectMilestone, ProjectStatus, ProjectDelivery, ProjectDeliveryTracker, ProjectDeliveryRating, \
    ProjectStatuses, EtlScheduler, Etl, EtlParameter, EtlParameterType, Gender, BusinessEventType, BusinessType, \
    Business, EducationLevel, BusinessStaff, Like, BusinessEvent, BusinessEventStaff, BusinessPatron, \
    BusinessPatronLike, BusinessPatronNetwork, BusinessEventPatronStatuses, BusinessEventPatronStatus, \
    BusinessEventRating, BusinessDiscoveryMethod, BusinessEventDiscover, MeetingAttendee, Meeting, MeetingType, \
    BCCCountry, BCCMembershipType, BCCHobby, BCCReasonJoin, BCCPerson, BCCStatus, BCCPersonStatus, BCCPersonHobby, \
    BCCDuesList, BCCRegistration, BCCPersonReasonJoin, BCCActivity, BCCVisit, BCCVisitActivity, BCCVisitNetwork, \
    BCCRelationship, BCCBarItem, BCCVesselType, BCCVesselSize, BCCVesselTypeSizePrice, BCCVessel, \
    BCCRelationshipType, BCCBarVisitTabPayment, BCCBarVisitTabPurchase, BCCBarVisitTab, BCCItemCategory, \
    BCCVisitRentalItem, BCCVisitRental, BCCArea
from flask_appbuilder import expose, BaseView, has_access, ModelView, action, CompactCRUDMixin
from flask_appbuilder.charts.views import DirectByChartView, ChartView
from flask_appbuilder.charts.views import GroupByChartView
from flask_appbuilder.models.group import aggregate_count, aggregate_sum, aggregate_avg
from flask_appbuilder.fieldwidgets import DateTimePickerWidget, Select2Widget
from flask_appbuilder.forms import DateTimeField
from flask_appbuilder.models.mongoengine.filters import FilterStartsWith, FilterEqualFunction

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
def get_filter_data(item_id,field):
    for obj in Project.objects:
        if obj._id == item_id:
            print(Project[field])
            return Project[field]


class EmployeeView(ModelView):
    datamodel = MongoEngineInterface(Employee)
    list_columns = ['name','gender','title','hourly_rate']


def get_startdate():
    return g.project.startdate_proposed


class ProjectView(ModelView):
    datamodel = MongoEngineInterface(Project)
    list_columns = ['name','owner','startdate_proposed','enddate_proposed','startdate_actual','enddate_actual']
    validators_columns = {
        'startdate_proposed': [StartDateValidate('enddate_proposed')],
        'startdate_actual': [StartDateValidate('enddate_actual')]
    }

class ProjectMilestoneView(ModelView):
    datamodel = MongoEngineInterface(ProjectMilestone)
    list_columns = ['project','owner','startdate_actual','enddate_actual','startdate_proposed','enddate_proposed']
    validators_columns = {
        'startdate_proposed': [StartDateValidate('enddate_proposed','milestone')],
        'startdate_actual': [StartDateValidate('enddate_actual','milestone')]
    }


class ProjectTaskView(ModelView):
    datamodel = MongoEngineInterface(ProjectTask)
    list_columns = ['milestone','owner','startdate_actual','enddate_actual',
                    'value_delivered']
    validators_columns = {
        'startdate_proposed': [StartDateValidate('enddate_proposed','task')],
        'startdate_actual': [StartDateValidate('enddate_actual','task')]
    }


class ProjectTypeView(ModelView):
    datamodel = MongoEngineInterface(ProjectType)


class ProjectDeliveryRatingView(ModelView):
    datamodel = MongoEngineInterface(ProjectDeliveryRating)
    list_columns = ['delivery','timestamp','rating','analyst']


class ProjectStatusView(ModelView):
    datamodel = MongoEngineInterface(ProjectStatus)
    list_columns = ['project','status','timestamp']

class ProjectStatusesView(ModelView):
    datamodel = MongoEngineInterface(ProjectStatuses)
    list_columns = ['status']

class ProjectDeliveryView(ModelView):
    datamodel = MongoEngineInterface(ProjectDelivery)
    list_columns = ['name', 'task','metric','unit','target','target_date']


class ProjectDeliveryTrackerView(ModelView):
    datamodel = MongoEngineInterface(ProjectDeliveryTracker)
    list_columns = ['delivery', 'stat','timestamp']


# ---------------- RISK ASSESSMENT ------------------
class RiskMatrixView(ModelView):
    datamodel = MongoEngineInterface(RiskMatrix)
    list_columns = ['name','project','analyst','analysis_date']


class RiskLikelihoodView(ModelView):
    datamodel = MongoEngineInterface(RiskLikelihood)
    list_columns = ['level','value', 'desc']


class RiskSeverityView(ModelView):
    datamodel = MongoEngineInterface(RiskSeverity)
    list_columns = ['level', 'value','desc']


class RiskView(ModelView):
    datamodel = MongoEngineInterface(Risk)
    list_columns = ['risk','matrix','category','desc','created_at']


class RiskAnalysisView(ModelView):
    datamodel = MongoEngineInterface(RiskAnalysis)
    list_columns = ['risk','likelihood','likelihood_comment','severity','severity_comment']


class RiskSolutionView(ModelView):
    datamodel = MongoEngineInterface(RiskSolution)
    list_columns = ['project','solution','suggestion_date']


class RiskCategoryView(ModelView):
    datamodel = MongoEngineInterface(RiskCategory)
    list_columns = ['name','desc']


# --------------------------------- ETL SCHEDULER ------------------------

class EtlView(ModelView):
    datamodel = MongoEngineInterface(Etl)

class EtlParameterTypeView(ModelView):
    datamodel = MongoEngineInterface(EtlParameterType)

class EtlParameterView(ModelView):
    datamodel = MongoEngineInterface(EtlParameter)
    list_columns = ['etl', 'type','label','handle','startdate']

# ------------------------------- CONSORTIUM --------------------------------
class GenderView(ModelView):
    datamodel = MongoEngineInterface(Gender)

class EducationLevelView(ModelView):
    datamodel = MongoEngineInterface(EducationLevel)


class BusinessTypeView(ModelView):
    datamodel = MongoEngineInterface(BusinessType)


class BusinessEventTypeView(ModelView):
    datamodel = MongoEngineInterface(BusinessEventType)


class BusinessView(ModelView):
    datamodel = MongoEngineInterface(Business)


class BusinessStaffView(ModelView):
    datamodel = MongoEngineInterface(BusinessStaff)

class Like(ModelView):
    datamodel = MongoEngineInterface(Like)


class BusinessEventView(ModelView):
    datamodel = MongoEngineInterface(BusinessEvent)


class BusinessEventStaffView(ModelView):
    datamodel = MongoEngineInterface(BusinessEventStaff)


class BusinessDiscoveryMethodView(ModelView):
    datamodel = MongoEngineInterface(BusinessDiscoveryMethod)


class BusinessDiscoverView(ModelView):
    datamodel = MongoEngineInterface(BusinessEventDiscover)


class BusinessPatronView(ModelView):
    datamodel = MongoEngineInterface(BusinessPatron)


class BusinessPatronLikeView(ModelView):
    datamodel = MongoEngineInterface(BusinessPatronLike)


class BusinessPatronNetworkView(ModelView):
    datamodel = MongoEngineInterface(BusinessPatronNetwork)


class BusinessEventPatronStatusesView(ModelView):
    datamodel = MongoEngineInterface(BusinessEventPatronStatuses)


class BusinessEventPatronStatusView(ModelView):
    datamodel = MongoEngineInterface(BusinessEventPatronStatus)


class BusinessEventRatingView(ModelView):
    datamodel = MongoEngineInterface(BusinessEventRating)


# #################################################


# ###############  MEETING ########################
class MeetingTypeView(ModelView):
    datamodel = MongoEngineInterface(MeetingType)


class MeetingView(ModelView):
    datamodel = MongoEngineInterface(Meeting)


class MeetingAttendeeView(ModelView):
    datamodel = MongoEngineInterface(MeetingAttendee)

###################################################

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


#######################################################################################################################
# ########################## CRUISING CLUB START *********************************************

class BCCCountryView(ModelView):
    datamodel = MongoEngineInterface(BCCCountry)


class BCCMembershipTypeView(ModelView):
    datamodel = MongoEngineInterface(BCCMembershipType)


class BCCHobbyView(ModelView):
    datamodel = MongoEngineInterface(BCCHobby)


class BCCReasonJoinView(ModelView):
    datamodel = MongoEngineInterface(BCCReasonJoin)


class BCCPersonView(ModelView):
    datamodel = MongoEngineInterface(BCCPerson)


class BCCStatusView(ModelView):
    datamodel = MongoEngineInterface(BCCStatus)


class BCCPersonStatusView(ModelView):
    datamodel = MongoEngineInterface(BCCPersonStatus)


class BCCPersonHobbyView(ModelView):
    datamodel = MongoEngineInterface(BCCPersonHobby)


class BCCDuesListView(ModelView):
    datamodel = MongoEngineInterface(BCCDuesList)


class BCCRelationshipTypeView(ModelView):
    datamodel = MongoEngineInterface(BCCRelationshipType)


class BCCRelationshipView(ModelView):
    datamodel = MongoEngineInterface(BCCRelationship)


class BCCPersonReasonJoinView(ModelView):
    datamodel = MongoEngineInterface(BCCPersonReasonJoin)


class BCCActivityView(ModelView):
    datamodel = MongoEngineInterface(BCCActivity)


class BCCVisitView(ModelView):
    datamodel = MongoEngineInterface(BCCVisit)
    list_columns = ['person','arrived','departed']


class BCCVisitActivityView(ModelView):
    datamodel = MongoEngineInterface(BCCVisitActivity)


class BCCVisitNetworkView(ModelView):
    datamodel = MongoEngineInterface(BCCVisitNetwork)

#  ## BAR
class BCCVesselTypeView(ModelView):
    datamodel = MongoEngineInterface(BCCVesselType)

class BCCAreaView(ModelView):
    datamodel = MongoEngineInterface(BCCArea)
    list_columns = ['area', 'description']

class BCCItemCategoryView(ModelView):
    datamodel = MongoEngineInterface(BCCItemCategory)
    list_columns = ['category','area', 'description']

class BCCBarItemView(ModelView):
    datamodel = MongoEngineInterface(BCCBarItem)
    list_columns = ['item','category', 'price']

class BCCBarVisitTabView(ModelView):
    datamodel = MongoEngineInterface(BCCBarVisitTab)
    list_columns = ['tab','visit','opened_at','amount']
    add_columns = ['visit']

class BCCBarVisitTabPurchaseView(ModelView):
    datamodel = MongoEngineInterface(BCCBarVisitTabPurchase)
    list_columns = ['tab','item','amount','total']


class BCCBarVisitTabPaymentView(ModelView):
    datamodel = MongoEngineInterface(BCCBarVisitTabPayment)
    list_columns = ['tab','payment']

#  VESSEL
class BCCVesselTypeView(ModelView):
    datamodel = MongoEngineInterface(BCCVesselType)


class BCCVesselSizeView(ModelView):
    datamodel = MongoEngineInterface(BCCVesselSize)


class BBCVesselTypeSizePriceView(ModelView):
    datamodel = MongoEngineInterface(BCCVesselTypeSizePrice)


class BCCVesselView(ModelView):
    datamodel = MongoEngineInterface(BCCVessel)


class BCCRegistrationView(ModelView):
    datamodel = MongoEngineInterface(BCCRegistration)

# ###########
class BCCVisitRentalItemView(ModelView):
    datamodel = MongoEngineInterface(BCCVisitRentalItem)
    list_columns = ['item','category','price','period','serial_no']

class BCCVisitRentalView(ModelView):
    datamodel = MongoEngineInterface(BCCVisitRental)
    list_columns = ['visit','item','timestamp_taken','timestamp_returned']


######################################################################################################################
##########################  CRUISING CLUB END ######################################################



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

# --------------------- MONGO VIEWS
appbuilder.add_view(ProjectView,
                    'Projects',
                    icon='fa-folder',
                    category='Projects')

appbuilder.add_view(EmployeeView,
                    'Staff',
                    icon='fa-users',
                    category='Projects')

appbuilder.add_view(ProjectMilestoneView,
                    'Milestones',
                    icon='fa-clipboard',
                    category='Projects')

appbuilder.add_view(ProjectTaskView,
                    'Tasks',
                    icon='fa-tasks',
                    category='Projects')

appbuilder.add_view(ProjectTypeView,
                    'Type',
                    icon='fa-folder',
                    category='Projects')


appbuilder.add_view(ProjectStatusView,
                    'Project status',
                    icon='fa-info',
                    category='Projects')

# -- Delivery rating
appbuilder.add_view(ProjectDeliveryView,
                    'Task Delivery',
                    icon='fa-check-square',
                    category='Projects')

appbuilder.add_view(ProjectDeliveryTrackerView,
                    'Delivery Tracker',
                    icon='fa-industry',
                    category='Projects')

appbuilder.add_view(ProjectDeliveryRatingView,
                    'Delivery rating',
                    icon='fa-star',
                    category='Projects')

appbuilder.add_view(ProjectStatusesView,
                    'Statuses',
                    icon='fa-star',
                    category='Projects')

# -- RISK
appbuilder.add_view(RiskCategoryView,
                    'Risk category',
                    icon='fa-tags',
                    category='Risk Assessment')

appbuilder.add_view(RiskSeverityView,
                    'Severity',
                    icon='fa-balance-scale',
                    category='Risk Assessment')

appbuilder.add_view(RiskLikelihoodView,
                    'Likelihood',
                    icon='fa-percent',
                    category='Risk Assessment')

appbuilder.add_view(RiskMatrixView,
                    'Risk Matrix',
                    icon='fa-th-large',
                    category='Risk Assessment')

appbuilder.add_view(RiskView,
                    'Risks',
                    icon='fa-exclamation-triangle',
                    category='Risk Assessment')

appbuilder.add_view(RiskSolutionView,
                    'Risk solutions',
                    icon='fa-ambulance',
                    category='Risk Assessment')

appbuilder.add_view(RiskAnalysisView,
                    'Risks analysis',
                    icon='fa-calculator',
                    category='Risk Assessment')

#   CHART VIEWS
appbuilder.add_view(EventChartView,
                    "Event charts",
                    icon="fa-dashboard",
                    category="Statistics")


#  ETL VIEWS
appbuilder.add_view(EtlView,
                    "ETLs",
                    icon="fa-bezier-curve",
                    category="ETLs")

appbuilder.add_view(EtlParameterTypeView,
                    "Parameter type",
                    icon="fa-clipboard-check",
                    category="ETLs")

appbuilder.add_view(EtlParameterView,
                    "Parameters",
                    icon="fa-clipboard-list",
                    category="ETLs")


# BUSINESS VIEWS
appbuilder.add_view(GenderView,
                    "Gender",
                    icon="fa-venus-mars",
                    category="Business")

appbuilder.add_view(EducationLevelView,
                    "Educational level",
                    icon="fa-graduation-cap",
                    category="Business")


appbuilder.add_view(BusinessTypeView,
                    "Company type",
                    icon="fa-briefcase",
                    category="Business")

appbuilder.add_view(BusinessEventTypeView,
                    "Company event type",
                    icon="fa-business-time",
                    category="Business")

appbuilder.add_view(BusinessView,
                    "Company info",
                    icon="fa-info",
                    category="Business")

appbuilder.add_view(BusinessStaffView,
                    "Employees",
                    icon="fa-id-badge",
                    category="Business")

appbuilder.add_view(Like,
                    "Hobbies and likes",
                    icon="fa-thumbs-up",
                    category="Business")

appbuilder.add_view(BusinessEventView,
                    "Event",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessEventStaffView,
                    "Event staff",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessDiscoveryMethodView,
                    "Company discovery options",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessDiscoverView,
                    "Event discovery",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessPatronView,
                    "Event patrons",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessPatronLikeView,
                    "Patron likes",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessPatronNetworkView,
                    "Patron networks",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessEventPatronStatusesView,
                    "Event patron status options",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessEventPatronStatusView,
                    "Event patron status",
                    icon="fa-long-arrow-down",
                    category="Business")

appbuilder.add_view(BusinessEventRatingView,
                    "Event rating",
                    icon="fa-long-arrow-down",
                    category="Business")


# ############### MEETING VIEW ############
appbuilder.add_view(MeetingTypeView,
                    "Meeting type",
                    icon="fa-long-arrow-down",
                    category="Meeting")

appbuilder.add_view(MeetingView,
                    "Meeting",
                    icon="fa-long-arrow-down",
                    category="Meeting")

appbuilder.add_view(MeetingAttendeeView,
                    "Meeeting Attendee",
                    icon="fa-long-arrow-down",
                    category="Meeting")

# ################## CRUISING CLUB START ######################################################################
##############################################################################################################


appbuilder.add_view(BCCCountryView,
                    "Country",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCMembershipTypeView,
                    "Membership Type",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCHobbyView,
                    "Member hobbies",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCReasonJoinView,
                    "Reasons for joining",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCPersonView,
                    "Club attendees",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCStatusView,
                    "Member status",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCPersonStatusView,
                    "Member statuses",
                    icon="fa-ship",
                    category="Cruising Club Registration")


appbuilder.add_view(BCCPersonHobbyView,
                    "Member hobbies",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCDuesListView,
                    "Dues by month",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCRelationshipTypeView,
                    "Relationship type",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCRelationshipView,
                    "Relationships",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCPersonReasonJoinView,
                    "Reasons for joining",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCActivityView,
                    "Club activities",
                    icon="fa-ship",
                    category="Cruising Club Visit")


appbuilder.add_view(BCCVisitActivityView,
                    "Member/Guest activity",
                    icon="fa-ship",
                    category="Cruising Club Visit")

appbuilder.add_view(BCCVisitNetworkView,
                    "Member Networks",
                    icon="fa-ship",
                    category="Cruising Club Visit")

appbuilder.add_view(BCCAreaView,
                    "Bcc Areas",
                    icon="fa-ship",
                    category="Cruising Club Rentals")

appbuilder.add_view(BCCItemCategoryView,
                    "BCC categories",
                    icon="fa-ship",
                    category="Cruising Club Rentals")

appbuilder.add_view(BCCVisitRentalItemView,
                    "Rental items",
                    icon="fa-ship",
                    category="Cruising Club Rentals")

appbuilder.add_view(BCCVisitRentalView,
                    "Rental",
                    icon="fa-ship",
                    category="Cruising Club Rentals")

appbuilder.add_view(BCCBarItemView,
                    "Bar items",
                    icon="fa-ship",
                    category="Cruising Club Bar")


appbuilder.add_view(BCCBarVisitTabView,
                    "Bar tabs",
                    icon="fa-ship",
                    category="Cruising Club Bar")


appbuilder.add_view(BCCBarVisitTabPurchaseView,
                    "Bar tab purchase",
                    icon="fa-ship",
                    category="Cruising Club Bar")


appbuilder.add_view(BCCBarVisitTabPaymentView,
                    "Bar tab payment",
                    icon="fa-ship",
                    category="Cruising Club Bar")

appbuilder.add_view(BCCVesselTypeView,
                    'Vessel Type',
                    icon="fa-ship",
                    category="Cruising Club Vessel")

appbuilder.add_view(BCCVesselSizeView,
                    "Vessel Size",
                    icon="fa-ship",
                    category="Cruising Club Vessel")


appbuilder.add_view(BBCVesselTypeSizePriceView,
                    "Type Size ",
                    icon="fa-ship",
                    category="Cruising Club Vessel")

appbuilder.add_view(BCCVesselView,
                    "Vessel info",
                    icon="fa-ship",
                    category="Cruising Club Vessel")

appbuilder.add_view(BCCRegistrationView,
                    "Registration page",
                    icon="fa-ship",
                    category="Cruising Club Registration")

appbuilder.add_view(BCCVisitView,
                    "Member/Guest visit info",
                    icon="fa-ship",
                    category="Cruising Club Visit")






######################################################################################################################
##########################  CRUISING CLUB END ######################################################

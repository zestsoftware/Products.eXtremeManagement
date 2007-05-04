from Acquisition import aq_inner
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *

eXtremeManagementTool_schema = BaseSchema.copy()


class eXtremeManagementTool(UniqueObject, BaseContent):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (getattr(UniqueObject,'__implements__',()),) + (getattr(BaseContent,'__implements__',()),)

    # This name appears in the 'add' box
    archetype_name = 'eXtremeManagementTool'

    meta_type = 'eXtremeManagementTool'
    portal_type = 'eXtremeManagementTool'
    allowed_content_types = []
    filter_content_types = 0
    global_allow = 0
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "eXtremeManagementTool"
    typeDescMsgId = 'description_edit_extrememanagementtool'
    _at_rename_after_creation = True
    schema = eXtremeManagementTool_schema

    # tool-constructors have no id argument, the id is fixed
    def __init__(self, id=None):
        BaseContent.__init__(self,'xm_tool')
        self.setTitle('eXtremeManagementTool')
        
    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()

    security.declarePublic('formatTime')
    def formatTime(self,time):
        """
        Returns time as a formatted string
        e.g. 3:15
        """
        hours = int(time)
        minutes = int(round((time - hours)*60))
        # Adjust for rounding:
        if minutes == 60:
            minutes = 0
            hours += 1
        if hours == 0 and minutes == 0:
            return ('0:00')
        minutes = abs(minutes)
        hours = abs(hours)
        minutes = self.formatMinutes(minutes)
        # This should not happen:
        if minutes is False:
            minutes = ':ERROR'
        sign = ''
        if time < 0:
            sign = '-'
        return ('%s%s%s' % (sign, hours, minutes))

    security.declarePublic('formatMinutes')
    def formatMinutes(self,minutes):
        """
        Takes the integer argument minutes and formats it nicely.  Examples:
        5  => :05
        24 => :24
        minutes should be between 0 and 59.
        """
        minutes = int(minutes)
        if minutes < 0:
            return False
        if minutes > 59:
            return False
        if minutes < 10:
            minutes = '0%s' % minutes
        minutes = ':%s' % minutes
        return minutes

    security.declarePublic('getProjectsToList')
    def getProjectsToList(self):
        """
        return all projects for the current user
        """
        pc = getToolByName(self, 'portal_catalog')
        brains = pc({'portal_type': 'Project', 'review_state': 'active'})
        for brain in brains:
            projects.append(brain.getObject())

        return projects

    security.declarePublic('getIssues')
    def getIssues(self,filter):
        """
        """
        pass

    security.declarePublic('getFilteredIssues')
    def getFilteredIssues(self, filter={}):
        """
        return issues (POI) that match the given filter.

        filter is a dictionary containing portal_catalog queries, eg:

        * filter = {} -> all issues are returned
        * filter = {'state': ['open','unconfirmed']} -> all
          open or unconfirmed issues are returned

        returs:
        { {'title':'issues for me', 'issues':[issue1,...]}, {'title':'issues from me', 'issues':[issue1,...]} }

        XXX At the moment this function never gets called.  Instead
        there is a getFilteredIssues python script in the skins dir.
        One of the two should be removed.  Maurits.
        """
        if not self.hasPoi():
            return []
        pc = getToolByName(self, 'portal_catalog')
        mtool = getToolByName(self, 'portal_membership')

        currentUser = mtool.getAuthenticatedMember().getId()

        grouped_issues = []

        # issues assigned to me
        issue_group = {'title': 'Issues assigned to me'}
        grouped_issues.append(issue_group)

        searchFilter = filter
        searchFilter['portal_type'] = 'PoiIssue'
        searchFilter['getResponsibleManager'] = currentUser

        issue_group['issues'] = pc(searchFilter)

        # issues created by me
        issue_group = {'title': 'Issues created by me'}
        grouped_issues.append(issue_group)

        searchFilter = filter
        searchFilter['portal_type'] = 'PoiIssue'
        searchFilter['Creator'] = currentUser

        issue_group['issues'] = pc(searchFilter)

        return grouped_issues

    security.declarePublic('hasPoi')
    def hasPoi(self):
        """True if Poi is available (though not necessarily installed,
        unfortonuately); False otherwise.
        """
        return HAS_POI

    def getStateSortedContents(self, items):
        """Get completed/invoiced items first, then rest of ordered folder contents
        """
        firstStates = ['completed', 'invoiced']
        firstItems = []
        otherItems = []
        for item in items:
            if item.review_state in firstStates:
                firstItems.append(item)
            else:
                otherItems.append(item)
        return firstItems + otherItems

    security.declarePublic('get_progress_perc')
    def get_progress_perc(self, part, total):
        """
        When you get above maximum_not_completed_percentage, and your
        story still is not completed, we deem it safer to display this
        percentage so as not to give a false sense of completeness.
        """
        context = self
        if total > 0:
            percentage = round(part/total*100, 1)
            portal_properties = getToolByName(context, 'portal_properties')
            xm_props = portal_properties.xm_properties
            if percentage > xm_props.maximum_not_completed_percentage:
                return xm_props.maximum_not_completed_percentage
            return percentage
        return 0


registerType(eXtremeManagementTool, PROJECTNAME)

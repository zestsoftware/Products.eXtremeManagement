from Acquisition import aq_inner
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName
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
        
    # tool should not appear in portal_catalog
    def at_post_edit_script(self):
        self.unindexObject()

    security.declarePublic('formatTime')
    def formatTime(self,time):
        """Returns time as a formatted string

        >>> xt = eXtremeManagementTool()
        >>> xt.formatTime(0)
        '0:00'
        >>> xt.formatTime(-0.6)
        '-0:36'
        >>> xt.formatTime(0.6)
        '0:36'
        >>> xt.formatTime(-1)
        '-1:00'
        >>> xt.formatTime(1)
        '1:00'
        >>> xt.formatTime(1.5)
        '1:30'
        >>> xt.formatTime(-1.5)
        '-1:30'

        Now try some times that might give problems, e.g.:
        .04*60 equals 2.3999999999999999, which should be rounded down

        >>> xt.formatTime(0.04)
        '0:02'
        >>> xt.formatTime(8.05)
        '8:03'
        >>> xt.formatTime(44.5)
        '44:30'
        >>> xt.formatTime(0.999)
        '1:00'

        """
        try:
            hours = int(time)
            minutes = int(round((time - hours)*60))
        except TypeError:
            return '?:??'
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
        """Takes the integer argument minutes and formats it nicely.

        >>> xt = eXtremeManagementTool()
        >>> xt.formatMinutes(0)
        ':00'
        >>> xt.formatMinutes(5)
        ':05'
        >>> xt.formatMinutes(42)
        ':42'
        >>> xt.formatMinutes(59)
        ':59'

        minutes should be between 0 and 59

        >>> xt.formatMinutes(-1)
        False
        >>> xt.formatMinutes(60)
        False

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
        """Get progress percentage of part compared to total.

        >>> xt = eXtremeManagementTool()
        >>> xt.get_progress_perc(3, 1)
        300

        We do not want to go over 100 percent though, so we have a
        setting in a property sheet that we use.  Set up a test
        environment for that.

        >>> xm_properties = dict(maximum_not_completed_percentage = 90)
        >>> portal_properties = dict()
        >>> portal_properties['xm_properties'] = xm_properties
        >>> xt.portal_properties = portal_properties

        Now try again.

        >>> xt.get_progress_perc(3, 1)
        90

        Code that uses this method can choose to show 100 percent to
        the user, for instance because a Story has the status
        'completed'.  But that is not our responsibility.

        Now for some more tests.

        >>> xt.get_progress_perc(0, 1)
        0
        >>> xt.get_progress_perc(10, 100)
        10
        >>> xt.get_progress_perc(1, 3)
        33
        >>> xt.get_progress_perc(1, 3.0)
        33

        """
        context = self
        if total > 0:
            try:
                percentage = int(round(part/float(total)*100))
            except TypeError:
                return '??'
            portal_properties = getToolByName(context, 'portal_properties', None)
            if portal_properties is None:
                return percentage
            xm_props = portal_properties.get('xm_properties', None)
            if xm_props is None:
                return percentage
            max_percentage = xm_props.get('maximum_not_completed_percentage', 90.0)
            if percentage > max_percentage:
                return max_percentage
            return percentage
        return 0


registerType(eXtremeManagementTool, PROJECTNAME)

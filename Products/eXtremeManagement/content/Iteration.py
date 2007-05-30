from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMIteration

schema = Schema((
    DateTimeField(
        name='startDate',
        validators=('isValidDate',),
        widget=CalendarWidget(
            show_hm=False,
            label='Start date',
            label_msgid='eXtremeManagement_label_startDate',
            i18n_domain='eXtremeManagement'),
    ),
    DateTimeField(
        name='endDate',
        validators=('isValidDate',),
        widget=CalendarWidget(
            show_hm=False,
            label='End date',
            label_msgid='eXtremeManagement_label_endDate',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='manHours',
        validators=('isInt',),
        widget=IntegerWidget(
            label='Man hours',
            label_msgid='eXtremeManagement_label_manHours',
            i18n_domain='eXtremeManagement'),
    ),
),)

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Iteration_schema = FolderSchema + schema


class Iteration(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__,)
    implements(IXMIteration)

    # This name appears in the 'add' box
    archetype_name = 'Iteration'
    portal_type = meta_type = 'Iteration'
    allowed_content_types = ['Story']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'iteration_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Iteration"
    typeDescMsgId = 'description_edit_iteration'
    _at_rename_after_creation = True
    schema = Iteration_schema

    security.declarePublic('startable')
    def startable(self):
        """
        Test if all stories in this iteration have statuses that are
        okay.  Usually that status should be 'estimated', but at least
        it should not be 'draft' or 'pending'.
        """
        unAcceptableStatuses = ['draft','pending']
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        stories = self.contentValues('Story')
        for story in stories:
            review_state = wf_tool.getInfoFor(story,'review_state')
            if review_state in unAcceptableStatuses:
                return False
        return True

    security.declarePublic('completable')
    def completable(self):
        """
        Test if all stories in this iteration have completed.
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        stories = self.contentValues('Story')
        for story in stories:
            review_state = wf_tool.getInfoFor(story,'review_state')
            if review_state != 'completed':
                return False
        return True

registerType(Iteration, PROJECTNAME)

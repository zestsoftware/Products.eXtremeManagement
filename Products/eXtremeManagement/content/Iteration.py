from zope.interface import implements
from AccessControl import ClassSecurityInfo

from DateTime import DateTime

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import CalendarWidget
from Products.Archetypes.atapi import DateTimeField
from Products.Archetypes.atapi import IntegerField
from Products.Archetypes.atapi import IntegerWidget
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import Schema

from Products.eXtremeManagement.interfaces import IXMIteration

schema = Schema((
    DateTimeField(
        name='startDate',
        validators=('isValidDate', ),
        widget=CalendarWidget(
            show_hm=False,
            label='Start date',
            label_msgid='eXtremeManagement_label_startDate',
            i18n_domain='eXtremeManagement'),
        default_method='defaultStartDate'
    ),
    DateTimeField(
        name='endDate',
        validators=('isValidDate', ),
        widget=CalendarWidget(
            show_hm=False,
            label='End date',
            label_msgid='eXtremeManagement_label_endDate',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='manHours',
        validators=('isInt', ),
        widget=IntegerWidget(
            label='Man hours',
            label_msgid='eXtremeManagement_label_manHours',
            i18n_domain='eXtremeManagement'),
    ),
), )

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Iteration_schema = FolderSchema + schema

UNACCEPTABLE_STATUSES = ['draft', 'pending']


class Iteration(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMIteration)

    # This name appears in the 'add' box
    archetype_name = 'Iteration'
    portal_type = meta_type = 'Iteration'
    typeDescription = "Iteration"
    typeDescMsgId = 'description_edit_iteration'
    _at_rename_after_creation = True
    schema = Iteration_schema

    security.declarePublic('getIteration')

    def getIteration(self):
        """
        Return self. Useful while doing aquisition down the tree.
        """
        return self

    security.declarePublic('startable')

    def startable(self):
        """
        Test if all stories in this iteration have statuses that are
        okay.  Usually that status should be 'estimated', but at least
        it should not be 'draft' or 'pending'.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        stories = self.contentValues(filter={'portal_type': 'Story'})
        for story in stories:
            review_state = wf_tool.getInfoFor(story, 'review_state')
            if review_state in UNACCEPTABLE_STATUSES:
                return False
        return True

    security.declarePublic('defaultStartDate')

    def defaultStartDate(self):
        """
        Return the current DateTime as default for the startDate.
        """
        return DateTime()
        security.declarePublic('completable')

    def completable(self):
        """
        Test if all stories in this iteration have completed.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        stories = self.contentValues(filter={'portal_type': 'Story'})
        for story in stories:
            review_state = wf_tool.getInfoFor(story, 'review_state')
            if review_state != 'completed':
                return False
        return True

    def duration(self):
        """
        Calculate the duration of this iteration in days
        """
        return int(round(self.endDate - self.startDate))

registerType(Iteration, 'eXtremeManagement')

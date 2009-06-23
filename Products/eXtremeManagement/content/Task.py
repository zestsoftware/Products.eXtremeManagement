import logging

from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import BaseFolder
from Products.Archetypes.atapi import BaseFolderSchema
from Products.Archetypes.atapi import DisplayList
from Products.Archetypes.atapi import InAndOutWidget
from Products.Archetypes.atapi import IntegerField
from Products.Archetypes.atapi import IntegerWidget
from Products.Archetypes.atapi import LinesField
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import SelectionWidget
from Products.Archetypes.atapi import TextField

from Products.eXtremeManagement.interfaces import IXMTask
from Products.eXtremeManagement.content.schemata import quarter_vocabulary


schema = Schema((
    TextField(
        name='mainText',
        allowable_content_types=('text/plain', 'text/structured',
                                 'text/html', 'application/msword', ),
        default_output_type='text/html',
        widget=RichWidget(
            label='Main text',
            label_msgid='eXtremeManagement_label_mainText',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='hours',
        default="0",
        label="Estimated hours",
        validators=('isInt', ),
        widget=IntegerWidget(
            description="Enter the estimated time (in hours).",
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            description_msgid='eXtremeManagement_help_hours',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='minutes',
        vocabulary=quarter_vocabulary,
        validators=('isInt', ),
        default="0",
        label="Estimated minutes",
        widget=SelectionWidget(
            description="Enter the rest of the estimated time in minutes",
            label='Minutes',
            label_msgid='eXtremeManagement_label_minutes',
            description_msgid='eXtremeManagement_help_minutes',
            i18n_domain='eXtremeManagement'),
    ),
    LinesField(
        name='assignees',
        multiValued=1,
        vocabulary='_get_assignees',
        widget=InAndOutWidget(
            description="Select the member(s) to assign this task to.",
            label='Assignees',
            label_msgid='eXtremeManagement_label_assignees',
            description_msgid='eXtremeManagement_help_assignees',
            i18n_domain='eXtremeManagement'),
    ),
), )

FolderSchema = BaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Task_schema = FolderSchema + schema


class Task(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (BaseFolder.__implements__, )
    implements(IXMTask)

    # This name appears in the 'add' box
    archetype_name = 'Task'
    portal_type = meta_type = 'Task'
    typeDescription = "Task"
    typeDescMsgId = 'description_edit_task'
    _at_rename_after_creation = True
    schema = Task_schema
    log = logging.getLogger("eXtremeManagement Task")

    # This looks like a nice and simple version of a ComputedField

    @property
    def estimate(self):
        return int(self.getHours()) + (int(self.getMinutes()) / 60.0)

    security.declarePublic('recalc')

    def recalc(self):
        """See the IEstimate interface.
        With our implementation we only need a reindex here actually.
        """
        self.reindexObject(idxs=['actual_time'])

    security.declarePublic('_get_assignees')

    def _get_assignees(self):
        """
        returns a list of team members
        """
        mt = getToolByName(self, 'portal_membership')
        md = getToolByName(self, 'portal_memberdata')
        # all the member that work on this project
        # XXX test if user folders somewhere else are recognized too
        employees = self.getProject().getMembers(role='Employee')
        assignables = []
        # build displaylist
        for memberId in employees:
            member = mt.getMemberById(memberId)
            if member is not None:
                fullname = member.getProperty('fullname', None)
                # if fullname is '' or None, return the id
                name = fullname and fullname.strip() or member.getId()
            else:
                name = memberId
            assignables.append((memberId, name))

        return DisplayList(assignables)

    security.declarePublic('CookedBody')

    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()


    security.declarePublic('startable')

    def startable(self):
        """Is the task startable?

        A task should have an estimate.

        Previously, we also required having an assignee, but not
        anymore: you should be able to start an iteration with all its
        stories and tasks and then developers can pick their tasks,
        without having them picked for them.
        """
        if (self.getHours() > 0 or self.getMinutes() > 0):
            return True
        return False

    def getDefaultAssignee(self):
        mem = getToolByName(self, 'portal_membership')
        currentUser = mem.getAuthenticatedMember().getId()
        if currentUser in self._get_assignees():
            return currentUser
        return ''


registerType(Task, 'eXtremeManagement')

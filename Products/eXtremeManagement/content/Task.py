import logging
from sets import Set

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
from Products.eXtremeManagement.Extensions.workflow_scripts import mailMessage
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
        default_method='getDefaultAssignee',
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
        return self.getHours() + (self.getMinutes() / 60.0)

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

    security.declarePublic('setAssignees')

    def setAssignees(self, value, **kw):
        """Overwrite the default setter.  Send an email should on assignment.

        But not when the Task is edited and the assignees don't
        change.  And if they _do_ change, then don't mail the people
        that were already assigned.

        Now why does setAssignees get called *three* times when a new
        Task is made???

        And why is the value a list which contains an empty item ''???

        Anyway, we need to do some serious checking.
        """
        if isinstance(value, basestring) and value:
            value = [value]
        elif not value:
            value = []
        else:
            value = list(Set([x for x in value if x]))
            value.sort()
        self.log.debug('New assignees value=%s.', value)
        old_assignees = list(Set([x for x in self.getAssignees()]))
        old_assignees.sort()
        self.schema['assignees'].set(self, value)

        # TODO: this should definitely be moved out into a event handler
        # as a content class should be pretty dumb, it should not know it
        # needs to send out emails ... separation of concerns - Rocky
        if self.REQUEST.get('SCHEMA_UPDATE', '0') == '1':
            # Schema update in progress!  We definitely do not want to
            # send emails now as that would be spamming.
            return

        portal_properties = getToolByName(self, 'portal_properties')
        xm_props = portal_properties.xm_properties
        if not xm_props.send_task_mails:
            return
        if old_assignees != value:
            self.log.debug('old_assignees=%s.', old_assignees)
            portal = getToolByName(self, 'portal_url').getPortalObject()
            new_employees = [x for x in value if x not in old_assignees]
            for employee in new_employees:
                self.log.debug('Sending email to %s for task %s.',
                               employee, self.id)
                mailMessage(portal, self, 'New Task assigned', employee)

    security.declarePublic('CookedBody')

    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()


    security.declarePublic('startable')

    def startable(self):
        """
        A task should have an assignee and either an estimate or a
        booking.
        """
        if len(self.getAssignees()) == 0:
            return False
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

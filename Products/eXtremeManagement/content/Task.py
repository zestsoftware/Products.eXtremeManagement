import logging
from sets import Set

from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *
from Products.CMFPlone.interfaces.NonStructuralFolder import INonStructuralFolder

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMTask
from Products.eXtremeManagement.Extensions.eXtreme_Task_Workflow_scripts import mailMessage

schema = Schema((
    TextField(
        name='mainText',
        allowable_content_types=('text/plain', 'text/structured', 'text/html', 'application/msword',),
        default_output_type='text/html',
        widget=RichWidget(
            label='Main text',
            label_msgid='eXtremeManagement_label_mainText',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='hours',
        default="0",
        index="FieldIndex",
        label="Estimated hours",
        validators=('isInt',),
        widget=IntegerWidget(
            description="Enter the estimated time (in hours).",
            label='Hours',
            label_msgid='eXtremeManagement_label_hours',
            description_msgid='eXtremeManagement_help_hours',
            i18n_domain='eXtremeManagement'),
    ),
    IntegerField(
        name='minutes',
        index="FieldIndex",
        vocabulary=(0, 15, 30, 45),
        validators=('isInt',),
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
        index="KeywordIndex:brains",
        multiValued=1,
        vocabulary='_get_assignees',
        default_method='getDefaultAssignee',
        widget=MultiSelectionWidget(
            description="Select the member(s) to assign this task to.",
            label='Assignees',
            label_msgid='eXtremeManagement_label_assignees',
            description_msgid='eXtremeManagement_help_assignees',
            i18n_domain='eXtremeManagement'),
    ),
    ComputedField(
        name='rawEstimate',
        index="FieldIndex:brains",
        widget=ComputedWidget(
            label='Estimate',
            label_msgid='eXtremeManagement_label_rawEstimate',
            i18n_domain='eXtremeManagement')
    ),
    ComputedField(
        name='rawActualHours',
        index="FieldIndex:brains",
        widget=ComputedWidget(
            label='Actual hours',
            label_msgid='eXtremeManagement_label_rawActualHours',
            i18n_domain='eXtremeManagement')
    ),
    ComputedField(
        name='rawDifference',
        index="FieldIndex:brains",
        widget=ComputedWidget(
            label='Difference',
            label_msgid='eXtremeManagement_label_rawDifference',
            i18n_domain='eXtremeManagement')
    ),
),)

FolderSchema = BaseFolderSchema.copy()
FolderSchema['description'].isMetadata = False
FolderSchema['description'].schemata = 'default'
Task_schema = FolderSchema + schema


class Task(BaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (BaseFolder.__implements__,)
    implements(IXMTask)

    # This name appears in the 'add' box
    archetype_name = 'Task'
    portal_type = meta_type = 'Task'
    allowed_content_types = ['Booking']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'task_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Task"
    typeDescMsgId = 'description_edit_task'
    allow_discussion = True
    _at_rename_after_creation = True
    schema = Task_schema
    log = logging.getLogger("eXtremeManagement Task")

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
                fullname =  member.getProperty('fullname', None)
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
        if old_assignees != value:
            self.log.debug('old_assignees=%s.', old_assignees)
            portal = getToolByName(self, 'portal_url').getPortalObject()
            if portal.hasProperty('xm_task_schema_updating'):
                self.log.debug('Task schema update, so not sending email '
                               'to %s for task %s.', value, self.id)
            else:
                new_employees = [x for x in value if x not in old_assignees]
                for employee in new_employees:
                    self.log.debug('Sending email to %s for task %s.',
                                   employee, self.id)
                    mailMessage(portal, self, 'New Task assigned',
                                employee, self.log)

    security.declarePublic('getRawEstimate')
    def getRawEstimate(self):
        """
        Return hours + minutes as a single float.
        """
        return self.getHours() + (self.getMinutes() / 60.0)

    security.declarePublic('getEstimate')
    def getEstimate(self):
        """
        Return the formatted estimate.
        """
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawEstimate())

    security.declarePublic('getRawActualHours')
    def getRawActualHours(self):
        """ Returns a float for further calculation.
        """
        actual = 0.0
        catalog = getToolByName(self, 'portal_catalog')
        searchpath = '/'.join(self.getPhysicalPath())
        bookings = catalog.searchResults(
            portal_type='Booking',
            path=searchpath)
        for booking in bookings:
            actual = actual + booking.getRawActualHours
        return actual

    security.declarePublic('getActualHours')
    def getActualHours(self):
        """Returns a formatted string
           e.g. 3:15
        """
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawActualHours())

    security.declarePublic('getRawDifference')
    def getRawDifference(self):
        """
        """
        return self.getRawActualHours() -  self.getRawEstimate()

    security.declarePublic('getDifference')
    def getDifference(self):
        """
        """
        xt = getToolByName(self, 'xm_tool')
        return xt.formatTime(self.getRawDifference())

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
        if not self.getAssignees():
            return False
        return self.getRawEstimate() > 0 or self.getRawActualHours() > 0

    def getDefaultAssignee(self):
        mem = getToolByName(self, 'portal_membership')
        currentUser = mem.getAuthenticatedMember().getId()
        if currentUser in self._get_assignees():
            return currentUser
        return ''

    def manage_afterAdd(self, item, container):
        # With Plone 2.1 we cannot use events reliably. :(
        super(Task, self).manage_afterAdd(item, container)
        self.reindexObject()

    def manage_afterClone(self, item):
        # With Plone 2.1 we cannot use events reliably. :(
        super(Task, self).manage_afterClone(item)
        self.reindexObject()

    def manage_pasteObjects(self, cb_copy_data=None, REQUEST=None):
        # With Plone 2.1 we cannot use events reliably. :(
        super(Task, self).manage_pasteObjects(cb_copy_data, REQUEST)
        self.reindexObject()

    def _delObject(self, orig_id, *args, **kwargs):
        super(Task, self)._delObject(orig_id, *args, **kwargs)
        self.reindexObject()

    def reindexObject(self, *args, **kwargs):
        # making eXtremeManagement portal_factory-aware is a bit gross but
        # as long as a Booking's state influences it's parent Task, we need
        # to make speed optimizations like this - Rocky
        factory = getToolByName(self, 'portal_factory')
        if not factory.isTemporary(self):
            super(Task, self).reindexObject(*args, **kwargs)
            parent = self.aq_inner.aq_parent
            parent.reindexObject()

registerType(Task, PROJECTNAME)

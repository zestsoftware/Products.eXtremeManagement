from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import *

from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.interfaces import IXMStory

schema = Schema((
    TextField(
        name='mainText',
        allowable_content_types=('text/plain', 'text/structured',
                                 'text/html', 'application/msword',),
        default_output_type='text/html',
        required=1,
        widget=RichWidget(
            description="Enter the main description for this object.",
            label='Main text',
            label_msgid='eXtremeManagement_label_mainText',
            description_msgid='eXtremeManagement_help_mainText',
            i18n_domain='eXtremeManagement'),
    ),
    FloatField(
        name='roughEstimate',
        write_permission="eXtremeManagement: Edit roughEstimate",
        validators=('isDecimal',),
        widget=DecimalWidget(
            description="Enter a rough estimate in days (tip: use multiples of 0.5 days)",
            label='Rough estimate',
            label_msgid='eXtremeManagement_label_roughEstimate',
            description_msgid='eXtremeManagement_help_roughEstimate',
            i18n_domain='eXtremeManagement'),
    ),
),)

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['id'].widget.visible = dict(edit=0, view=0)
Story_schema = FolderSchema + schema


class Story(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__,)
    implements(IXMStory)

    # This name appears in the 'add' box
    archetype_name = 'Story'
    portal_type = meta_type = 'Story'
    allowed_content_types = ['Task']
    filter_content_types = 1
    global_allow = 0
    content_icon = 'story_icon.gif'
    immediate_view = 'base_view'
    default_view = 'base_view'
    suppl_views = ()
    typeDescription = "Story"
    typeDescMsgId = 'description_edit_story'
    allow_discussion = True
    _at_rename_after_creation = True
    schema = Story_schema

    security.declarePublic('CookedBody')
    def CookedBody(self):
        """
        Dummy attribute to allow drop-in replacement of Document
        """
        return self.getMainText()

    security.declarePublic('generateUniqueId')
    def generateUniqueId(self, type_name):
        """ Generate sequential IDs for tasks
        With thanks to Upfront Systems for their code from Upfront Project
        """
        if type_name == 'Task':
            tasks = self.getStoryTasks()
            taskids = [0]
            for task in tasks:
                try:
                    taskid = task.getId()
                    taskids.append(int(taskid))
                except:
                    print 'WARNING: non-integer taskid found: %s' % taskid
            lastTaskId = max(taskids) + 1
            return str(lastTaskId)
        else:
            return self.aq_parent.generateUniqueId(type_name)

    security.declarePublic('isCompleted')
    def isCompleted(self):
        """
        Returns True is the Story has review_state 'completed'.
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        state = wf_tool.getInfoFor(self, 'review_state')
        return state == 'completed'

    security.declarePublic('isEstimated')
    def isEstimated(self):
        """
        True when roughEstimate is set.  Actually, it could be an old
        Story which does not have a roughEstimate.  That is okay, as
        long as the story has tasks that have an estimate.  The
        roughEstimate is superfluous in that case.  So checking the
        raw estimate is good.
        """
        return self.getRoughEstimate() > 0

    security.declarePublic('startable')
    def startable(self):
        """
        Test if all tasks in this story can be activated and if the
        Story itself has been estimated.  If the story is somehow
        already in-progress or completed, then that is fine as well.
        """
        unAcceptableStatuses = ['draft','pending']
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        review_state = wf_tool.getInfoFor(self,'review_state')
        if review_state in unAcceptableStatuses:
            return False
        if not self.isEstimated():
            return False
        tasks = self.getStoryTasks()
        if not tasks:
            return False
        else:
            for task in tasks:
                if not task.startable():
                    return False
            return True

    security.declarePublic('completable')
    def completable(self):
        """
        Test if all tasks in this iteration have completed.
        """
        portal = getToolByName(self,'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        tasks = self.getStoryTasks()
        for task in tasks:
            review_state = wf_tool.getInfoFor(task,'review_state')
            if review_state != 'completed':
                return False
        return True

    security.declarePublic('getStoryTasks')
    def getStoryTasks(self):
        """return the tasks of this story
        """
        return self.contentValues(filter={'portal_type': ['Task', 'PoiTask']})


registerType(Story, PROJECTNAME)

import logging
from zope.interface import implements
from AccessControl import ClassSecurityInfo

from Products.CMFCore.utils import getToolByName
from Products.Archetypes.atapi import DecimalWidget
from Products.Archetypes.atapi import FloatField
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import OrderedBaseFolderSchema
from Products.Archetypes.atapi import registerType
from Products.Archetypes.atapi import RichWidget
from Products.Archetypes.atapi import Schema
from Products.Archetypes.atapi import TextField

from Products.eXtremeManagement.interfaces import IXMStory

log = logging.getLogger("eXtremeManagement Story")


schema = Schema((
    TextField(
        name='mainText',
        default_output_type='text/html',
        widget=RichWidget(
            description="Enter the main description for this object.",
            rows='20',
            label='Main text',
            label_msgid='eXtremeManagement_label_mainText',
            description_msgid='eXtremeManagement_help_mainText',
            i18n_domain='eXtremeManagement'),
    ),
    FloatField(
        name='roughEstimate',
        write_permission="eXtremeManagement: Edit roughEstimate",
        validators=('isDecimal', ),
        widget=DecimalWidget(
            description="Enter a rough estimate in days "
                        "(tip: use multiples of 0.5 days)",
            label='Rough estimate',
            label_msgid='eXtremeManagement_label_roughEstimate',
            description_msgid='eXtremeManagement_help_roughEstimate',
            i18n_domain='eXtremeManagement'),
    ),
), )

FolderSchema = OrderedBaseFolderSchema.copy()
FolderSchema['id'].widget.visible = dict(edit=0, view=0)
Story_schema = FolderSchema + schema


class Story(OrderedBaseFolder):
    """
    """
    security = ClassSecurityInfo()
    __implements__ = (OrderedBaseFolder.__implements__, )
    implements(IXMStory)

    # This name appears in the 'add' box
    archetype_name = 'Story'
    portal_type = meta_type = 'Story'
    typeDescription = "Story"
    typeDescMsgId = 'description_edit_story'
    _at_rename_after_creation = True
    schema = Story_schema

    @property
    def size_estimate(self):
        "return the size estimate on a story in days"
        if self.getRoughEstimate():
            return self.getRoughEstimate()
        else:
            return 0.0

    security.declarePublic('recalc')

    def set_size_estimate(self, val):
        """Set the rough estimate and update the catalog"""
        self.setRoughEstimate(val)
        self.recalc()

    def recalc(self):
        """See the ISizeEstimate interface.
        With our implementation we only need a reindex here actually.
        """
        self.reindexObject(idxs=['size_estimate'])

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
        if type_name in ('Task', 'PoiTask'):
            ids = self.contentIds()
            intids = [0]
            for id_ in ids:
                try:
                    intids.append(int(id_))
                except:
                    pass
            new_id = max(intids) + 1
            return str(new_id)
        else:
            return self.aq_parent.generateUniqueId(type_name)

    security.declarePublic('isCompleted')

    def isCompleted(self):
        """
        Returns True if the Story has review_state 'completed'.
        """
        portal = getToolByName(self, 'portal_url').getPortalObject()
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
        unAcceptableStatuses = ['draft', 'pending']
        portal = getToolByName(self, 'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        review_state = wf_tool.getInfoFor(self, 'review_state')
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
        portal = getToolByName(self, 'portal_url').getPortalObject()
        wf_tool = getToolByName(portal, 'portal_workflow')
        tasks = self.getStoryTasks()
        for task in tasks:
            review_state = wf_tool.getInfoFor(task, 'review_state')
            if review_state != 'completed':
                return False
        return True

    security.declarePublic('getStoryTasks')

    def getStoryTasks(self):
        """return the tasks of this story
        """
        return self.contentValues(filter={'portal_type': ['Task', 'PoiTask']})


registerType(Story, 'eXtremeManagement')

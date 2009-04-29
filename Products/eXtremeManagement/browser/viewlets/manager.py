import logging

from Acquisition import Explicit
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.exceptions import DiscussionNotAllowed
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.interface import implements

from interfaces import ISimpleTaskList
from interfaces import ISimpleStoryList
from interfaces import IStoryDetails
from interfaces import IStoryDetailsBox

logger = logging.getLogger('story_viewlet')


class SimpleTaskListManager(Explicit):
    implements(ISimpleTaskList)
    template = ViewPageTemplateFile('templates/manage_simple_tasklist.pt')
    render = template
    realtasks = None
    show_story = False

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

        try:
            self.tasks = view.tasklist()
        except AttributeError:
            self.tasks = None

    def update(self):
        pass


class SimpleStoryListManager(Explicit):
    implements(ISimpleStoryList)
    template = ViewPageTemplateFile('templates/manage_simple_storylist.pt')
    render = template
    realstories = None
    iteration_object = None
    iteration_dict = None
    show_iteration = False
    show_progress = False
    show_totals = False
    iteration_number = '1'

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def iteration_icon(self):
        # the (1) is needed otherwise getIcon() will return
        # 'plone/iteration_icon.gif', which is wrong. The template
        # will add the $portal_url prefix
        return self.iteration_object.getIcon(1)

    def update(self):
        pass


class StoryDetailsProvider(Explicit):
    implements(IStoryDetails)
    template = ViewPageTemplateFile('templates/manage_story_details.pt')
    render = template
    story_object = None
    number_of_comments = 0

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        uid = request.get('uid')
        if uid is not None:
            brains = getToolByName(context, 'uid_catalog')(UID=uid)
            self.story_object = brains[0].getObject()
            pd = getToolByName(context, 'portal_discussion')
            try:
                replies = pd.getDiscussionFor(self.story_object).getReplies()
            except DiscussionNotAllowed:
                replies = []
            self.number_of_comments = len(replies)
        self.__parent__ = view

    def update(self):
        pass


class StoryDetailsBox(Explicit):
    """Details box within a story view.
    """
    implements(IStoryDetailsBox)
    template = ViewPageTemplateFile('templates/story_details_box.pt')
    render = template
    story_object = None
    number_of_comments = 0

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        uid = request.get('uid')
        if uid is not None:
            brains = getToolByName(context, 'uid_catalog')(UID=uid)
            self.story_object = brains[0].getObject()
            if self.story_object.portal_type != 'Story':
                logger.warn('object %s is not a story.', self.story_object)
                self.story_object = None
        if self.story_object is None:
            self.story_object = context
        self.__parent__ = view

    def update(self):
        pass

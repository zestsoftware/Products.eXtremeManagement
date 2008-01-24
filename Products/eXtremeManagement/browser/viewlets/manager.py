from Acquisition import Explicit
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewlet
from zope.component import getUtility, getAdapters
from zope.component import getMultiAdapter, queryMultiAdapter
from interfaces import ISimpleTaskList
from zope.interface import implements


class SimpleTaskListManager(Explicit):
    implements(ISimpleTaskList)
    template = ViewPageTemplateFile('templates/manage_simple_tasklist.pt')
    render = template
    realtasks = None

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

        # XXX All views should have the same method here.
        try:
            self.tasks = view.tasks()
        except AttributeError:
            self.tasks = view.tasklist()

    def update(self):
        pass

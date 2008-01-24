from Acquisition import Explicit
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from interfaces import ISimpleTaskList
from zope.interface import implements


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

"""
The old plone2 portlet ported to plone3

The filename is painful and confusing; should change it here,
the ZCML, and the test file.
"""

from zope.component import getMultiAdapter
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class ITasksPortlet(IPortletDataProvider):
    """This defines the configurable options (if any) for the portlet.

    It will be used to generate add and edit forms.
    """
    pass


class Assignment(base.Assignment):
    """The assignment is a persistent object used to store the
    configuration of a particular instantiation of the portlet.
    """

    implements(ITasksPortlet)

    def __init__(self, show_date=True, show_time=True, sitewide=True):
        self.show_date = show_date
        self.show_time = show_time
        self.sitewide = sitewide

    @property
    def title(self):
        return u"Personal administration"


class Renderer(base.Renderer):

    # render() will be called to render the portlet
    render = ViewPageTemplateFile('portlet_tasks.pt')

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        tools = getMultiAdapter((context, request),
                                             name=u'plone_tools')
        portal_state = getMultiAdapter((context, request),
                                            name=u'plone_portal_state')
        self.anonymous = portal_state.anonymous()
        self.mtool = tools.membership()
        self.portal_url = portal_state.portal_url()

    @property
    def available(self):
        """Determine if the portlet is available at all.
           We only want to show this portlet to employees"""
        return not self.anonymous and \
            self.mtool.checkPermission("eXtremeManagement: Add Booking",
                                       self.context)


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        return Assignment()

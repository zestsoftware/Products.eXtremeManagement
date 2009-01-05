"""
The old plone2 portlet ported to plone3

The filename is painful and confusing; should change it here,
the ZCML, and the test file.
"""

from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from plone.app.portlets.portlets import base
from plone.portlets.interfaces import IPortletDataProvider
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


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

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see
# base.Assignment).


class Renderer(base.Renderer):

    def __init__(self, context, request, view, manager, data):
        base.Renderer.__init__(self, context, request, view, manager, data)
        self.membership = getToolByName(self.context, 'portal_membership')
        self.context_state = getMultiAdapter((context, request),
                                             name=u'plone_context_state')
        url_tool = getToolByName(self.context, 'portal_url')
        self.portal = url_tool.getPortalObject()
        self.portal_state = getMultiAdapter((context, request),
                                            name=u'plone_portal_state')
        self.pas_info = getMultiAdapter((context, request), name=u'pas_info')

    # render() will be called to render the portlet
    render = ViewPageTemplateFile('portlet_tasks.pt')

    def available(self):
        return not self.portal_state.anonymous()

    def portal_url(self):
        return self.portal_state.portal_url()

    def hasManagePermission(self):
        return self.membership.checkPermission('Manage Portal', self.context)


# Define the add forms and edit forms, based on zope.formlib. These use
# the interface to determine which fields to render.


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        return Assignment()

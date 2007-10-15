"""Define a portlet that doesn't do much besides show the date.
Just a test before we try something real.
"""

from zope import schema
from zope.component import getMultiAdapter
from zope.formlib import form
from zope.interface import implements
from zope.component import getMultiAdapter, queryMultiAdapter, getUtility


from plone.app.portlets.portlets import base
from plone.memoize.instance import memoize
from plone.portlets.interfaces import IPortletDataProvider

from DateTime import DateTime
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.CMFCore.utils import getToolByName

import datetime

# This interface defines the configurable options (if any) for the portlet.
# It will be used to generate add and edit forms.
# If both show_date and show_time are False the portlet should be suppressed.

class ITasksPortlet(IPortletDataProvider):
    pass



# The assignment is a persistent object used to store the configuration of
# a particular instantiation of the portlet.
# ?? Why do I have to set default values above and in __init_() ?

class Assignment(base.Assignment):
    implements(ITasksPortlet)

    def __init__(self, show_date=True, show_time=True, sitewide=True):
        self.show_date = show_date
        self.show_time = show_time
        self.sitewide = sitewide

    @property
    def title(self):
        return u"Tasks"

# The renderer is like a view (in fact, like a content provider/viewlet). The
# item self.data will typically be the assignment (although it is possible
# that the assignment chooses to return a different object - see 
# base.Assignment).

class Renderer(base.Renderer):
    
    def __init__(self, context, request, view, manager, data):
            base.Renderer.__init__(self, context, request, view, manager, data)
            
            self.membership = getToolByName(self.context, 'portal_membership')
            
            self.context_state = getMultiAdapter((context, request), name=u'plone_context_state')
            self.portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
            self.pas_info = getMultiAdapter((context, request), name=u'pas_info')

    # render() will be called to render the portlet
    
    render = ViewPageTemplateFile('tasks_portlet.pt')
       
    # The 'available' property is used to determine if the portlet should
    # be shown. Suppress if we don't show date or time.
        
    available = True
    #@property
    #def available(self):
    #    return self.show_date or self.show_time

    # To make the view template as simple as possible, we return dicts with
    # only the necessary information.


    
    def isAnon(self):
        return self.portal_state.anonymous()
    
    def portal_url(self):
        return self.portal_state.portal_url()
    
    def portal(self):
        return self.portal_state.portal()
    
    def hasManagePermission(self):
        return self.membership.checkPermission('Manage Portal', self.context)
        
        
    
# Define the add forms and edit forms, based on zope.formlib. These use
# the interface to determine which fields to render.

class AddForm(base.AddForm):
    form_fields = form.Fields(ITasksPortlet)
    label = (u"Add Tasks portlet")
    description = (u"This portlet displays tasks.")

    # This method must be implemented to actually construct the object.
    # The 'data' parameter is a dictionary, containing the values entered
    # by the user.

    def create(self, data):
        assignment = Assignment()
        form.applyChanges(assignment, self.form_fields, data)
        return assignment

class EditForm(base.EditForm):
    form_fields = form.Fields(ITasksPortlet)
    label = (u"Edit tasks portlet")
    description = (u"This portlet displays tasks")

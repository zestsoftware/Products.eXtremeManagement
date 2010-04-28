from Acquisition import aq_inner

from zope.component import getMultiAdapter
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.eXtremeManagement import XMMessageFactory as _


class IIterationsPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    implements(IIterationsPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Iterations')


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('iterations.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        tools = getMultiAdapter((self.context, self.request),
                                        name=u'plone_tools')
        self.site_url = portal_state.portal_url()
        self.portal = portal_state.portal()
        self.project = self._get_project()
        self.catalog = tools.catalog()
        self.project_url = self.project and self.project.absolute_url() or None

    @property
    def available(self):
        """Determine if the portlet is available at all."""
        return self.project and self.iterations()

    def _get_project(self):
        """This property return the url of the current project, if not within
        a project it returns None
        """
        try:
            #If we are inside a project aqcuisition will find it
            project = aq_inner(self.context).getProject()
        except AttributeError:
            # Or raise an error, in which case we return None
            project = None
        return project

    @memoize
    def current(self):
        path = '/'.join(self.project.getPhysicalPath())
        brains = self.catalog.searchResults(portal_type='Iteration',
                                       review_state='in-progress',
                                       path=path)
        # By default return a link to the first iteration found.
        # Other iteration will return a link to the second one and is shown as
        # a status message
        if brains:
            return brains[0].getURL()
        else:
            return False

    @memoize
    def iterations(self):
        """ This method returns all links that should be shown in the Portlet.
        The returned dataset is as follows:

        result = [{'title': 'completed',
                   'iterations': [{'url': 'http://somewhere.com',
                                   'title': 'Some where'}],
                 }]

        If no links are available it returns None

        """
        results = []
        states = dict()
        if self.project:
            cfilter = {'portal_type': 'Iteration'}
            brains = self.project.getFolderContents(cfilter)
            for brain in brains:
                wf_state = brain.review_state
                url = brain.getURL()
                title = brain.Title
                item = {'title': title, 'url': url}
                if wf_state != 'in-progress':
                    if not wf_state in states.keys():
                        states[wf_state] = [item]
                    else:
                        states[wf_state].append(item)
        for state in states.keys():
            iterations = states[state]
            results.append({'title': state,
                            'iterations': iterations})
        return results

    def has_finished_iterations(self):
        """Do we have finished iterations?"""
        states = [item['title'] for item in self.iterations()]
        if 'invoiced' in states:
            return True
        if 'completed' in states:
            return True
        if 'own-account' in states:
            return True
        return False

    def has_planned_iterations(self):
        """Do we have planned iterations?"""
        states = [item['title'] for item in self.iterations()]
        if 'new' in states:
            return True
        return False


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        return Assignment()

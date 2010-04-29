from Acquisition import aq_inner

from zope.component import getMultiAdapter, ComponentLookupError
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from plone.memoize.view import memoize

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.eXtremeManagement import XMMessageFactory as _


class IProjectPortlet(IPortletDataProvider):
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
    implements(IProjectPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Project links')


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('project.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        portal_state = getMultiAdapter((self.context, self.request),
                                        name=u'plone_portal_state')
        self.site_url = portal_state.portal_url()
        self.portal = portal_state.portal()
        self.project = self._get_project()
        self.project_url = self.project and self.project.absolute_url() or None

    @property
    def available(self):
        """Determine if the portlet is available at all."""
        if self.project and self.links():
            return True

    def _get_project(self):
        """This property return the url of the current project, if not within
        a project it return site_url
        """
        try:
            #If we are inside a project aqcuisition will find it
            project = aq_inner(self.context).getProject()
        except AttributeError:
            # Or raise an error, in which case we return None
            project = None
        return project

    @memoize
    def links(self):
        """ This method returns all links that should be shown in the Portlet.
        The returned dataset is as follows:

        result = [{'url':'http://somewhere.com',
                   'title':'Somewhere',
                   'class':'odd/even'}]

        If no links are available it returns None

        """
        results = []
        if self.project:
            tracker = self.tracker_url()
            attachments = self.attachments_url()
            offers = self.offers_url()
            # chart = self.chart_url()
            results.append(dict(url=self.project_url, title=_(u'Project')))
            if tracker:
                results.append(dict(url=tracker, title=_(u'Issues')))
            if attachments:
                results.append(dict(url=attachments, title=_(u'Attachments')))
            if offers:
                results.append(dict(url=offers, title=_(u'Offer')))
            # if chart:
            #    results.append(dict(url=chart, title=_(u'Overview Chart')))
        for res in results:
            row = (results.index(res)+1)%2 and 'odd' or 'even'
            res['class'] = 'portletItem ' + row
        return results

    @memoize
    def tracker_url(self):
        """Return the url to the tracker, if available.
        We expect this call only occurs when self.project is not None
        """
        cfilter = {'portal_type': 'PoiTracker'}
        brains = self.project.getFolderContents(cfilter)
        if brains and len(brains) > 0:
            return brains[0].getURL()

        # Fallback; this used to be the default case.
        # See http://plone.org/products/extreme-management-tool/issues/207
        if 'issues' in self.project.objectIds():
            return self.project_url + '/issues'

    @memoize
    def attachments_url(self):
        """Return the url to the attachments view, if available.
        We expect this call only occurs when self.project is not None
        """
        cfilter = {'portal_type': ('File', 'Image', 'Story')}
        brains = self.project.getFolderContents(cfilter)
        if brains and len(brains) > 0:
            return self.project_url + '/project_content?type=other'
        return None

    @memoize
    def offers_url(self):
        """ Return the url to the offer, if available
        We expect this call only occurs when self.project is not None
        """
        cfilter = {'portal_type': ('Offer', )}
        brains = self.project.getFolderContents(cfilter)
        if brains and len(brains) == 1:
            return brains[0].getURL
        elif brains and len(brains) > 1:
            return self.project_url + '/project_content?type=offer'
        return None

    def chart_url(self):
        """ Return the url to the chart overview, if it has data"""
        try:
            chart = getMultiAdapter((self.project, self.request),
                                            name=u'chart')
        except ComponentLookupError:
            return None

        if chart.has_data():
            return self.project_url + '/@@chart_view'
        return None


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        return Assignment()

from Acquisition import aq_inner, aq_parent
from zope.component import getMultiAdapter


class XMIssueGetter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def get_issues(self, **kwargs):
        """Get a list of issue brains.

        This implementation will just traverse to the xm-poi view
        and call its get_open_issues_in_project method

        """
        project = self._lookup_project()
        if project is None:
            return []
        assert project.portal_type == 'Project', (
            "Failed to get associated project.")
        tools = getMultiAdapter((self.context, self.request),
                                 name=u'plone_tools')
        catalog = tools.catalog()
        query = dict(portal_type='PoiIssue',
                     review_state=['in-progress', 'open',
                                   'unconfirmed', 'new'],
                     path='/'.join(project.getPhysicalPath()))
        query.update(kwargs)
        return catalog(**query)

    def _lookup_project(self):
        item = aq_inner(self.context)
        while (item is not None and
               getattr(item, 'portal_type', None) != 'Project'):
            item = aq_parent(item)
        return item

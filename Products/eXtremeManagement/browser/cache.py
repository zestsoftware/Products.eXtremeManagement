from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName


class CacheHelperView(BrowserView):
    """Provide some helper methods for caching.

    A browser view makes sure we don't do this too many times without
    need.
    """

    def copy_happening(self):
        """Return whether a copy is happening inside a folder.
        """

        request = self.request
        copying = request.get('__cp', False)
        if copying:
            return 'copying'
        else:
            return 'not_copying'

    def my_hours(self):
        """Return my # of hours."""
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        daytotal = portal.restrictedTraverse('@@daytotal')
        return daytotal.total()

    def my_projects(self):
        """Return hash of my projects."""
        context = aq_inner(self.context)
        portal = getToolByName(context, 'portal_url').getPortalObject()
        projects = portal.restrictedTraverse('@@myprojects/projectlist')
        uids = [project.UID for project in projects]
        uid_string = ' '.join(uids)
        return str(hash(uid_string))

    def etag(self):
        """Return normal extra ETag components.

        Only location is used as an extra differentiator now, but
        later the current display and current default page should be
        added.
        """

        params = [self.copy_happening(),
                  self.my_hours(),
                  self.my_projects(),
                  ]
        return ';'.join(params)

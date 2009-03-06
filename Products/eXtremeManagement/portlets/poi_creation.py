from zope.component import getMultiAdapter
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.eXtremeManagement import XMMessageFactory as _


class IPoiCreationPortlet(IPortletDataProvider):
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
    implements(IPoiCreationPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Create tasks from issues')


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('poi_creation.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        self.poi_view = getMultiAdapter((self.context, self.request),
                                        name=u'xm-poi')

    @property
    def available(self):
        """Determine if the portlet is available at all.

        It is available when we are allowed to add a PoiTask here and
        there are open issues.
        """
        return self.poi_view.can_add_tasks() and \
            len(self.poi_view.get_open_issues_in_project()) > 0

    def available_tags(self):
        return self.poi_view.available_tags()


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        return Assignment()

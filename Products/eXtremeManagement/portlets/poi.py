from zope.component import getMultiAdapter
from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from Products.eXtremeManagement import XMMessageFactory as _


class IPoiPortlet(IPortletDataProvider):
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
    implements(IPoiPortlet)

    def __init__(self):
        pass

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return _(u'Related XM Tasks')


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """

    render = ViewPageTemplateFile('poi.pt')

    def __init__(self, *args):
        base.Renderer.__init__(self, *args)
        poi_view = getMultiAdapter((self.context, self.request),
                                        name=u'xm-poi')
        self.links = poi_view.links()
        self.stories = poi_view.stories_to_add_to()

    @property
    def available(self):
        """Determine if the portlet is available at all."""
        return (self.context.portal_type == 'PoiIssue'
                and (self.links or self.stories))


class AddForm(base.NullAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """

    def create(self):
        return Assignment()

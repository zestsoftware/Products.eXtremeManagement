from zope.component import getUtility, getMultiAdapter, queryMultiAdapter

from plone.portlets.interfaces import IPortletType
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletDataProvider
from plone.portlets.interfaces import IPortletRenderer

from Products.eXtremeManagement.portlets import portlet_tasks
from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase

from plone.app.portlets.storage import PortletAssignmentMapping

from plone.app.portlets.tests.base import PortletsTestCase


class TestPortlet(PortletsTestCase, eXtremeManagementTestCase):

    def afterSetUp(self):
        self.setRoles(('Manager', ))

    def testPortletTypeRegistered(self):
        portlet = getUtility(
            IPortletType, name='eXtremeManagement.TasksPortlet')
        self.assertEquals(portlet.addview, 'eXtremeManagement.TasksPortlet')

    def testInterfaces(self):
        portlet = portlet_tasks.Assignment()
        self.failUnless(IPortletAssignment.providedBy(portlet))
        self.failUnless(IPortletDataProvider.providedBy(portlet.data))

    def testInvokeAddview(self):
        portlet = getUtility(
            IPortletType, name='eXtremeManagement.TasksPortlet')

        mapping = self.portal.restrictedTraverse(
            '++contextportlets++plone.leftcolumn')
        for m in mapping.keys():
            del mapping[m]
        addview = mapping.restrictedTraverse('+/' + portlet.addview)

        # TasksPortal has a configurator that's currently empty
        # so give it empty data.  If it had no configurator just
        # call 'addview'
        #addview.createAndAdd(data={})
        addview()

        self.assertEquals(len(mapping), 1)
        self.failUnless(isinstance(mapping.values()[0],
                                   portlet_tasks.Assignment))

    def testInvokeEditView(self):
        mapping = PortletAssignmentMapping()
        request = self.folder.REQUEST

        mapping['foo'] = portlet_tasks.Assignment()
        editview = queryMultiAdapter(
            (mapping['foo'], request), name='edit', default=None)
        self.failUnless(isinstance(mapping.values()[0],
                                   portlet_tasks.Assignment))

    def testRenderer(self):
        context = self.folder
        request = self.folder.REQUEST
        view = self.folder.restrictedTraverse('@@plone')
        manager = getUtility(
            IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = portlet_tasks.Assignment()

        renderer = getMultiAdapter(
            (context, request, view, manager, assignment), IPortletRenderer)
        self.failUnless(isinstance(renderer, portlet_tasks.Renderer))


class TestRenderer(PortletsTestCase):

    def renderer(self, context=None, request=None, view=None, manager=None,
                 assignment=None):
        context = context or self.folder
        request = request or self.folder.REQUEST
        view = view or self.folder.restrictedTraverse('@@plone')
        manager = manager or getUtility(
            IPortletManager, name='plone.leftcolumn', context=self.portal)
        assignment = assignment or portlet_tasks.Assignment()

        return getMultiAdapter((context, request, view, manager, assignment),
                               IPortletRenderer)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPortlet))
    suite.addTest(makeSuite(TestRenderer))
    return suite

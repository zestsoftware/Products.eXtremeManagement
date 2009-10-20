from zope.component import getUtilitiesFor
from plone.app.workflow.interfaces import ISharingPageRole
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase
from Products.PloneTestCase.setup import default_user
from DateTime import DateTime


class testSetup(eXtremeManagementTestCase):
    """ Test cases for the generic setup of the product
    """

    def test_types(self):
        """
        """
        ids = self.portal.portal_types.objectIds()
        self.failUnless('Project' in ids)
        self.failUnless('Iteration' in ids)
        self.failUnless('Offer' in ids)
        self.failUnless('Story' in ids)
        self.failUnless('Task' in ids)
        self.failUnless('PoiTask' in ids)
        self.failUnless('Booking' in ids)

        # BBB can be removed in release 2.1
        self.failUnless('CustomerFolder' in ids)
        self.failUnless('Customer' in ids)
        self.failUnless('ProjectMember' in ids)
        self.failUnless('ProjectFolder' in ids)

    def test_skins(self):
        """
        """
        ids = self.portal.portal_skins.objectIds()
        self.failUnless('eXtremeManagement' in ids)

    def test_workflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('eXtreme_Project_Workflow' in ids)
        self.failUnless('eXtreme_Iteration_Workflow' in ids)
        self.failUnless('eXtreme_Offer_Workflow' in ids)
        self.failUnless('eXtreme_Story_Workflow' in ids)
        self.failUnless('eXtreme_Task_Workflow' in ids)
        self.failUnless('eXtreme_Default_Workflow' in ids)
        self.failUnless('folder_workflow' in ids)

    def test_workflowChains(self):
        getChain = self.portal.portal_workflow.getChainForPortalType
        self.failUnless('eXtreme_Project_Workflow' in getChain('Project'))
        self.failUnless('eXtreme_Iteration_Workflow' in getChain('Iteration'))
        self.failUnless('eXtreme_Offer_Workflow' in getChain('Offer'))
        self.failUnless('eXtreme_Story_Workflow' in getChain('Story'))
        self.failUnless('eXtreme_Task_Workflow' in getChain('Task'))
        self.failUnless('eXtreme_Task_Workflow' in getChain('PoiTask'))
        self.failUnless('eXtreme_Booking_Workflow' in getChain('Booking'))

        # BBB can be removed in release 2.1
        self.failUnless('folder_workflow' in getChain('CustomerFolder'))
        self.failUnless('folder_workflow' in getChain('ProjectFolder'))
        self.failUnless('eXtreme_Customer_Workflow' in getChain('Customer'))
        self.failUnless(
            'eXtreme_Default_Workflow' in getChain('ProjectMember'))

    def test_customizePortal(self):
        """
        """
        props_tool = getToolByName(self.portal, 'portal_properties')
        nav_props = props_tool.navtree_properties
        if nav_props.hasProperty(
            'rolesSeeUnpublishedContent'):
            rolesSeeUnpublishedContent = nav_props.getProperty(
                'rolesSeeUnpublishedContent')
            self.failUnless('Customer' in rolesSeeUnpublishedContent)

        if nav_props.hasProperty('metaTypesNotToList'):
            metaTypesNotToList = nav_props.getProperty('metaTypesNotToList')
            for ptype in ('Booking', 'Task', 'ProjectMember'):
                self.failUnless(ptype in metaTypesNotToList)

    def test_extraLocalRoles(self):
        """Test whether Employee and Customer have been added to the sharing
        tab roles.

        """
        names = [name for (name, utility) in
                 getUtilitiesFor(ISharingPageRole)]
        self.failUnless('Employee' in names)
        self.failUnless('Customer' in names)

    def testReinstall(self):
        """Reinstalling should not empty our indexes.
        """
        # First of all, our indexes should already be in the catalog
        # at this point.
        catalog = self.portal.portal_catalog
        wanted = ("getAssignees", "getBookingDate")
        indexes = catalog.indexes()
        for idx in wanted:
            self.failUnless(idx in indexes)

        def results(**kwargs):
            # Small helper function.
            return len(catalog.searchResults(**kwargs))

        # Something should be in the catalog already.
        oneday = DateTime(2000, 1, 1)
        self.assertEquals(results(portal_type='Task',
                                  getAssignees=default_user), 1)
        self.assertEquals(results(getBookingDate=oneday), 1)

        # Now we reinstall.
        quickinstaller = self.portal.portal_quickinstaller
        quickinstaller.reinstallProducts(['eXtremeManagement'])

        # Now we should still have a match.
        self.assertEquals(results(portal_type='Task',
                                  getAssignees=default_user), 1)
        self.assertEquals(results(getBookingDate=oneday), 1)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSetup))
    return suite

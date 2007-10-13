from zope.component import getUtilitiesFor
from plone.app.workflow.interfaces import ISharingPageRole
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

class testSetup(eXtremeManagementTestCase):
    """ Test cases for the generic setup of the product
    """

    def afterSetUp(self):
        """
        """
        pass

    def test_types(self):
        """
        """
        ids = self.portal.portal_types.objectIds()
        self.failUnless('CustomerFolder' in ids)
        self.failUnless('Customer' in ids)
        self.failUnless('ProjectMember' in ids)
        self.failUnless('ProjectFolder' in ids)
        self.failUnless('Project' in ids)
        self.failUnless('Iteration' in ids)
        self.failUnless('Story' in ids)
        self.failUnless('Task' in ids)
        self.failUnless('Booking' in ids)

    def test_skins(self):
        """
        """
        ids = self.portal.portal_skins.objectIds()
        self.failUnless('eXtremeManagement' in ids)

    def test_workflows(self):
        ids = self.portal.portal_workflow.objectIds()
        self.failUnless('eXtreme_Project_Workflow' in ids)
        self.failUnless('eXtreme_Iteration_Workflow' in ids)
        self.failUnless('eXtreme_Story_Workflow' in ids)
        self.failUnless('eXtreme_Task_Workflow' in ids)
        self.failUnless('eXtreme_Default_Workflow' in ids)
        self.failUnless('folder_workflow' in ids)

    def test_workflowChains(self):
        getChain = self.portal.portal_workflow.getChainForPortalType

        self.failUnless('eXtreme_Project_Workflow' in getChain('Project'))
        self.failUnless('eXtreme_Iteration_Workflow' in getChain('Iteration'))
        self.failUnless('eXtreme_Story_Workflow' in getChain('Story'))
        self.failUnless('eXtreme_Task_Workflow' in getChain('Task'))
        self.failUnless('eXtreme_Task_Workflow' in getChain('PoiTask'))
        self.failUnless('folder_workflow' in getChain('CustomerFolder'))
        self.failUnless('folder_workflow' in getChain('ProjectFolder'))
        self.failUnless('eXtreme_Customer_Workflow' in getChain('Customer'))
        self.failUnless('eXtreme_Booking_Workflow' in getChain('Booking'))
        self.failUnless('eXtreme_Default_Workflow' in getChain('ProjectMember'))

    def test_customizePortal(self):
        """
        """
        props_tool = getToolByName(self.portal, 'portal_properties')
        if props_tool.navtree_properties.hasProperty('rolesSeeUnpublishedContent'):
            rolesSeeUnpublishedContent = props_tool.navtree_properties.getProperty('rolesSeeUnpublishedContent')
            self.failUnless('Customer' in rolesSeeUnpublishedContent)

        if props_tool.navtree_properties.hasProperty('metaTypesNotToList'):
            metaTypesNotToList = props_tool.navtree_properties.getProperty(
                'metaTypesNotToList')
            for ptype in ('Booking','Task','ProjectMember'):
                self.failUnless(ptype in metaTypesNotToList)

    def test_testCustomizePortal(self):
        """
        """
        #Uncomment one of the following lines as needed

    def test_extraLocalRoles(self):
        """Test whether Employee and Customer have been added to the sharing
        tab roles.

        """
        names = [name for (name, utility) in
                 getUtilitiesFor(ISharingPageRole)]
        self.failUnless('Employee' in names)
        self.failUnless('Customer' in names)

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testSetup))
    return suite

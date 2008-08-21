from Products.eXtremeManagement.tests.base import eXtremeManagementTestCase

# Import our interfaces
from Products.eXtremeManagement.interfaces import IXMBooking
from Products.eXtremeManagement.interfaces import IXMCustomer
from Products.eXtremeManagement.interfaces import IXMCustomerFolder
from Products.eXtremeManagement.interfaces import IXMIteration
from Products.eXtremeManagement.interfaces import IXMOffer
from Products.eXtremeManagement.interfaces import IXMProject
from Products.eXtremeManagement.interfaces import IXMProjectFolder
from Products.eXtremeManagement.interfaces import IXMProjectMember
from Products.eXtremeManagement.interfaces import IXMStory
from Products.eXtremeManagement.interfaces import IXMTask

# Import our content types
from Products.eXtremeManagement.content.Booking import Booking
from Products.eXtremeManagement.content.Iteration import Iteration
from Products.eXtremeManagement.content.Offer import Offer
from Products.eXtremeManagement.content.Project import Project
from Products.eXtremeManagement.content.Story import Story
from Products.eXtremeManagement.content.Task import Task

# BBB can be removed in release 2.1
from Products.eXtremeManagement.content.ProjectFolder import ProjectFolder
from Products.eXtremeManagement.content.ProjectMember import ProjectMember
from Products.eXtremeManagement.content.Customer import Customer
from Products.eXtremeManagement.content.CustomerFolder import CustomerFolder


class testCase(eXtremeManagementTestCase):
    """Are we implementing the right interfaces?
    """

    def test_interfaces(self):
        self.failUnless(IXMBooking.implementedBy(Booking))
        self.failUnless(IXMBooking.providedBy(Booking('blah')))

        self.failUnless(IXMIteration.implementedBy(Iteration))
        self.failUnless(IXMIteration.providedBy(Iteration('blah')))

        self.failUnless(IXMOffer.implementedBy(Offer))
        self.failUnless(IXMOffer.providedBy(Offer('blah')))

        self.failUnless(IXMProject.implementedBy(Project))
        self.failUnless(IXMProject.providedBy(Project('blah')))

        self.failUnless(IXMStory.implementedBy(Story))
        self.failUnless(IXMStory.providedBy(Story('blah')))

        self.failUnless(IXMTask.implementedBy(Task))
        self.failUnless(IXMTask.providedBy(Task('blah')))

        # BBB can be removed in release 2.1
        self.failUnless(IXMCustomer.implementedBy(Customer))
        self.failUnless(IXMCustomer.providedBy(Customer('blah')))

        self.failUnless(IXMCustomerFolder.implementedBy(CustomerFolder))
        self.failUnless(IXMCustomerFolder.providedBy(CustomerFolder('blah')))

        self.failUnless(IXMProjectFolder.implementedBy(ProjectFolder))
        self.failUnless(IXMProjectFolder.providedBy(ProjectFolder('blah')))

        self.failUnless(IXMProjectMember.implementedBy(ProjectMember))
        self.failUnless(IXMProjectMember.providedBy(ProjectMember('blah')))


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testCase))
    return suite

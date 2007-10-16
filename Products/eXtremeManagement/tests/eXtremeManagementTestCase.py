import os, sys, code

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.eXtremeManagement.config import PRODUCT_DEPENDENCIES
from Products.eXtremeManagement.config import DEPENDENCIES
from Products.eXtremeManagement.timing.interfaces import IActualHours
from Products.eXtremeManagement.timing.interfaces import IEstimate


PRODUCT_DEPENDENCIES.append('eXtremeManagement')

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

ZopeTestCase.installProduct('eXtremeManagement')

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('eXtremeManagement')
PloneTestCase.setupPloneSite(products=PRODUCTS)

class eXtremeManagementTestCase(PloneTestCase.PloneTestCase):
    """Base TestCase for eXtremeManagement."""

    def assertObjectBrainEquality(self, attribute, value, obj, portal_type):
        """Test equality of object and its brain from the catalog.
        """
        brains = self.catalog(portal_type=portal_type,
                              path='/'.join(obj.getPhysicalPath()))
        # Get the first brain
        brain = brains[0]
        # Assert that attribute of object has the correct value
        self.assertEqual(obj[attribute](), value)
        # Assert that the brain has the same value
        self.assertEqual(brain[attribute], value)

    def assertTaskBrainEquality(self, attribute, value, task=None):
        if task is None:
            # Use default task
            task = self.task
        return self.assertObjectBrainEquality(attribute, value, task, portal_type='Task')

    def assertAnnotationGeneralBrainHoursEquality(self, obj, value, portal_type):
        ann = IActualHours(obj)
        self.assertEqual(ann.actual_time, value)
        brains = self.catalog(portal_type=portal_type,
                              path='/'.join(obj.getPhysicalPath()))
        self.assertEqual(brains[0]['actual_time'], value)

    def assertAnnotationTaskBrainHoursEquality(self, obj, value):
        self.assertAnnotationGeneralBrainHoursEquality(obj, value, 'Task')

    def assertAnnotationStoryBrainHoursEquality(self, obj, value):
        self.assertAnnotationGeneralBrainHoursEquality(obj, value, 'Story')

    def assertAnnotationGeneralBrainEstimateEquality(self, obj, value, portal_type):
        ann = IEstimate(obj)
        self.assertEqual(ann.estimate, value)
        brains = self.catalog(portal_type=portal_type,
                              path='/'.join(obj.getPhysicalPath()))
        self.assertEqual(brains[0]['estimate'], value)

    def assertAnnotationStoryBrainEstimateEquality(self, obj, value):
        self.assertAnnotationGeneralBrainEstimateEquality(obj, value, 'Story')

    def assertAnnotationTaskBrainEstimateEquality(self, obj, value):
        self.assertAnnotationGeneralBrainEstimateEquality(obj, value, 'Task')



class eXtremeManagementFunctionalTestCase(PloneTestCase.FunctionalTestCase, eXtremeManagementTestCase):
    """Base TestCase for eXtremeManagement."""


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(eXtremeManagementTestCase))
    return suite

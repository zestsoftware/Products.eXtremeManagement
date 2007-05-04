import os, sys, code

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.eXtremeManagement.config import HAS_PLONE21
from Products.eXtremeManagement.config import PRODUCT_DEPENDENCIES
from Products.eXtremeManagement.config import DEPENDENCIES

# Add common dependencies
if not HAS_PLONE21:
    DEPENDENCIES.append('Archetypes')
    PRODUCT_DEPENDENCIES.append('MimetypesRegistry')
    PRODUCT_DEPENDENCIES.append('PortalTransforms')
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


class eXtremeManagementFunctionalTestCase(PloneTestCase.FunctionalTestCase, eXtremeManagementTestCase):
    """Base TestCase for eXtremeManagement."""


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(eXtremeManagementTestCase))
    return suite

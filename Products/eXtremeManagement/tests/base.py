from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from xm.booking.timing.interfaces import IActualHours
from xm.booking.timing.interfaces import IEstimate

ztc.installProduct('Poi')
ztc.installProduct('eXtremeManagement')

@onsetup
def xm_setup():
    """Set up our Plone Site.
    """
    fiveconfigure.debug_mode = True
    import xm.booking
    import xm.portlets
    zcml.load_config('configure.zcml', xm.booking)
    zcml.load_config('configure.zcml', xm.portlets)
    fiveconfigure.debug_mode = False


xm_setup()
ptc.setupPloneSite(products=['eXtremeManagement'])

class eXtremeManagementTestCase(ptc.PloneTestCase):
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



class eXtremeManagementFunctionalTestCase(ptc.FunctionalTestCase, eXtremeManagementTestCase):
    """Base TestCase for eXtremeManagement."""

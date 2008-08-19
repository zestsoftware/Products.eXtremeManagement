import transaction
from AccessControl import SecurityManagement
from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Products.PloneTestCase.layer import PloneSite
from Products.PloneTestCase.setup import default_user
from Products.CMFPlone.utils import _createObjectByType
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
    zcml.load_config('configure.zcml', xm.booking)
    import xm.portlets
    zcml.load_config('configure.zcml', xm.portlets)
    fiveconfigure.debug_mode = False


xm_setup()
ptc.setupPloneSite(products=['eXtremeManagement'])


def login_as_portal_owner(app):
    uf = app.acl_users
    owner = uf.getUserById(ptc.portal_owner)
    if not hasattr(owner, 'aq_base'):
        owner = owner.__of__(uf)
    SecurityManagement.newSecurityManager(None, owner)
    return owner


def setup_xm_content_and_roles():
    app = ztc.app()
    owner = login_as_portal_owner(app)
    portal = getattr(app, ptc.portal_name)

    membership = portal.portal_membership
    # Setup global roles.
    membership.addMember('manager', 'secret', ['Manager'], [])
    membership.addMember('employee', 'secret', ['Employee'], [])
    membership.addMember('developer', 'secret', ['Employee'], [])
    membership.addMember('projectmanager', 'secret', ['Projectmanager'],
                         [])

    # Create Project directly in the Plone Site root.  We use a helper
    # method for this that does not bother us with authentication.
    _createObjectByType('Project', portal, 'project')
    project = portal.project

    # Give the local role Employee on this project to the default user.
    membership.setLocalRoles(project, [default_user], 'Employee')

    # Create Offer plus Story.
    _createObjectByType('Offer', project, 'offer')
    offer = project.offer
    _createObjectByType('Story', offer, 'story')
    offerstory = offer.story
    offerstory.update(roughEstimate=1.5)

    # Create Iteration etc.
    _createObjectByType('Iteration', project, 'iteration')
    iteration = project.iteration
    _createObjectByType('Story', iteration, 'story')
    story = iteration.story
    story.update(roughEstimate=1.5)
    workflow = portal.portal_workflow
    workflow.doActionFor(story, 'estimate')
    _createObjectByType('Task', story, 'task')
    task = story.task
    task.update(hours=5)
    task.update(minutes=30)

    _createObjectByType('Booking', task, 'booking', hours=3, minutes=15)
    booking = task.booking
    booking.setCreators(default_user)


class XMLayer(PloneSite):
    """Test layer that sets up some content and roles for xm.
    """

    @classmethod
    def setUp(cls):
        ptc.setupPloneSite(products=['eXtremeManagement'])
        PloneSite.setUp()
        setup_xm_content_and_roles()
        transaction.commit()


class eXtremeManagementTestCase(ptc.PloneTestCase):
    """Base TestCase for eXtremeManagement."""
    #layer = XMLayer

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
        return self.assertObjectBrainEquality(
            attribute, value, task, portal_type='Task')

    def assertAnnotationGeneralBrainHoursEquality(self, obj, value,
                                                  portal_type):
        ann = IActualHours(obj)
        self.assertEqual(ann.actual_time, value)
        brains = self.catalog(portal_type=portal_type,
                              path='/'.join(obj.getPhysicalPath()))
        self.assertEqual(brains[0]['actual_time'], value)

    def assertAnnotationTaskBrainHoursEquality(self, obj, value):
        self.assertAnnotationGeneralBrainHoursEquality(obj, value, 'Task')

    def assertAnnotationStoryBrainHoursEquality(self, obj, value):
        self.assertAnnotationGeneralBrainHoursEquality(obj, value, 'Story')

    def assertAnnotationGeneralBrainEstimateEquality(self, obj, value,
                                                     portal_type):
        ann = IEstimate(obj)
        self.assertEqual(ann.estimate, value)
        brains = self.catalog(portal_type=portal_type,
                              path='/'.join(obj.getPhysicalPath()))
        self.assertEqual(brains[0]['estimate'], value)

    def assertAnnotationStoryBrainEstimateEquality(self, obj, value):
        self.assertAnnotationGeneralBrainEstimateEquality(obj, value, 'Story')

    def assertAnnotationTaskBrainEstimateEquality(self, obj, value):
        self.assertAnnotationGeneralBrainEstimateEquality(obj, value, 'Task')


class eXtremeManagementFunctionalTestCase(ptc.FunctionalTestCase,
                                          eXtremeManagementTestCase):
    """Base TestCase for eXtremeManagement."""

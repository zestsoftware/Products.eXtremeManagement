from zope.event import notify
from zope.lifecycleevent import ObjectModifiedEvent
from Products.PloneTestCase.setup import default_user


def afterSetUp(self):
    """Test classes can use this as their afterSetUp method

    It adds most of our content types to the portal so that we have
    some basic data to test with.
    """

    self.default_user = default_user
    self.catalog = self.portal.portal_catalog
    self.workflow = self.portal.portal_workflow
    self.membership = self.portal.portal_membership

    self.loginAsPortalOwner()
    self.membership.addMember('manager', 'secret', ['Manager'], [])
    self.membership.addMember('employee', 'secret', ['Employee'], [])
    self.membership.addMember('developer', 'secret', ['Employee'], [])
    self.membership.addMember('projectmanager', 'secret', ['Projectmanager'],
                              [])
    self.portal.invokeFactory('Folder', id='projects')
    self.projects = self.folder.projects
    self.projects.invokeFactory('Project', id='project')
    self.project = self.projects.project
    self.membership.setLocalRoles(self.project, [default_user], 'Employee')
    self.project.invokeFactory('Offer', id='offer')
    self.offer = self.project.offer
    self.offer.invokeFactory('Story', id='story')
    self.offerstory = self.offer.story
    self.offerstory.update(roughEstimate=1.5)
    self.project.invokeFactory('Iteration', id='iteration')
    self.iteration = self.project.iteration
    self.iteration.invokeFactory('Story', id='story')
    self.story = self.iteration.story
    self.story.update(roughEstimate=1.5)
    self.workflow.doActionFor(self.story, 'estimate')
    #self.login('developer')
    self.story.invokeFactory('Task', id='task')
    self.task = self.story.task
    self.task.update(hours=5)
    self.task.update(minutes=30)
    self.login(default_user)
    self.task.invokeFactory('Booking', id='booking', hours=3, minutes=15)
    self.booking = self.task.booking
    self.setRoles([])


def createBooking(container, id=id, hours=0, minutes=0):
    """Create a Booking and fire the ObjectModifiedEvent.

    The event is fired automatically for you when you press Save in
    the edit form, but in testing we apparently need to take care of
    it ourselves.
    """
    container.invokeFactory('Booking', id=id)
    booking = container[id]
    booking.update(hours=hours, minutes=minutes)
    notify(ObjectModifiedEvent(booking))

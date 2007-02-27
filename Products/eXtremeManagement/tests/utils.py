def afterSetUp(self):
    """Test classes can use this as their afterSetUp method

    It adds most of our content types to the portal so that we have
    some basic data to test with.
    """

    self.catalog = self.portal.portal_catalog
    self.workflow = self.portal.portal_workflow
    self.membership = self.portal.portal_membership

    self.setRoles(['Manager'])
    self.membership.addMember('employee', 'secret', ['Employee'], [])
    self.membership.addMember('developer', 'secret', ['Employee'], [])
    self.portal.invokeFactory('ProjectFolder', id='projects')
    self.projects = self.folder.projects
    self.projects.invokeFactory('Project', id='project')
    self.project = self.projects.project
    self.project.invokeFactory('Iteration', id='iteration')
    self.iteration = self.project.iteration
    self.iteration.invokeFactory('Story', id='story')
    self.story = self.iteration.story
    self.story.setRoughEstimate(1.5)
    self.workflow.doActionFor(self.story, 'estimate')
    self.story.invokeFactory('Task', id='task')
    self.task = self.story.task
    self.task.invokeFactory('Booking', id='booking', hours=3, minutes=15)
    self.booking = self.task.booking
    self.setRoles([])

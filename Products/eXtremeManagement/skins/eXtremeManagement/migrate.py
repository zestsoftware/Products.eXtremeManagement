## Script (Python) "migrate"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title='Migrate eXtreme Management CTs'
##

def migrate_tasks(self, out):
    """
    Simply add 1 hour to the estimate of all tasks,
    for testing.
    """
    task_brains = self.portal_catalog(meta_type='Task')
    for task_brain in task_brains:
        task = task_brain.getObject()
        old_estimate = task.getEstimate() or 0
        new_estimate = old_estimate + 1
        task.setEstimate(new_estimate)
        print >> out, "Task title: %s" % task.title
        print >> out, "Old estimate: %s" % old_estimate
        print >> out, "New estimate: %s" % new_estimate
    print >> out, "Migration of tasks completed"


def migrate(self):
    """Run the migration"""

    out = StringIO()
    print >> out, "Starting migration"

    portal_url = getToolByName(self, 'portal_url')
    portal = portal_url.getPortalObject()

    self.migrate_tasks(out)

    print >> out, "Migration finished"
    return out.getvalue()

print container.migrate()
#print out.getvalue()
return printed

from Products.CMFCore.utils import getToolByName
from StringIO import StringIO

def migratePreWorkflowUninstall(self, out):
    portal = getToolByName(self, 'portal_url').getPortalObject()
    wf_tool = getToolByName(portal, 'portal_workflow')
    unwantedReviewStates = ('assigned', 'estimated', 'in-progress',)
    tasks_brains = portal.portal_catalog(meta_type='Task',
                                         review_state=unwantedReviewStates)
    for task_brain in tasks_brains:
        print >> out, task_brain
        task = task_brain.getObject()
        try:
            old_state = wf_tool.getInfoFor(task,'review_state')
        except:
            print >> out, 'No official review state found...'
            old_state = task_brain.review_state
            
        if task.hasProperty('xm_old_state') and \
           task.getProperty('xm_old_state') != old_state:
            print >> out, 'ERROR: migration for Task "%s" may not work.' \
                  % task.title_or_id()
            print >> out, 'Existing xm_old_state = %s.' % task.xm_old_state
            print >> out, 'Wanted xm_old_state = %s.' % old_state
        else:
            task.manage_addProperty('xm_old_state', old_state, 'string')

        # transition deactivate: in-progress -> estimated
        # transition reestimate: estimated   -> assigned
        # transition reject:     assigned    -> open
        if wf_tool.getInfoFor(task,'review_state') == 'in-progress':
            wf_tool.doActionFor(task, 'deactivate')
        if wf_tool.getInfoFor(task,'review_state') == 'estimated':
            wf_tool.doActionFor(task, 'reestimate')
        if wf_tool.getInfoFor(task,'review_state') == 'assigned':
            wf_tool.doActionFor(task, 'reject')
        if wf_tool.getInfoFor(task,'review_state') != 'open':
            print >> out, 'ERROR: Task "%s" failed to transition to open.' \
                  % task.title_or_id()
        task.reindexObject()
        task = task_brain.getObject()
    
    return out.getvalue()

def migrateAfterWorkflowInstall(self, out):
    """
    Migration from pre release svn trunk to release 1.0.
    Task with status assigned or estimated get status open.
    Task with status in-progress get status to-do.
    The old status has been saved in the property xm_old_state.
    Remove that property.
    """
    portal = getToolByName(self, 'portal_url').getPortalObject()
    wf_tool = getToolByName(portal, 'portal_workflow')
    tasks_brains = portal.portal_catalog(meta_type='Task',
                                         review_state='open')
    warnings = 0
    errors = 0
    for task_brain in tasks_brains:
        task = task_brain.getObject()
        if task.hasProperty('xm_old_state'):
            old_state = task.getProperty('xm_old_state')
            current_state = wf_tool.getInfoFor(task,'review_state')
            if old_state == 'in-progress':
                wanted_state = 'to-do'
            else:
                wanted_state = 'open'
            task.manage_delProperties(ids=('xm_old_state',))
            if wanted_state != current_state:
                if task.startable():
                    try:
                        wf_tool.doActionFor(task, 'activate')
                    except:
                        errors = errors + 1
                        print >> out, '------------------'
                        print >> out, 'ERROR: Transition to to-do failed.'
                        print >> out, 'Task name: %s' % task.title_or_id()
                        print >> out, 'URL: %s' % task.absolute_url()
                        print >> out, 'Staying in open state.'
                    task.reindexObject()
                else:
                    warnings = warnings + 1
                    print >> out, '------------------'
                    print >> out, 'WARNING: old in-progress task not startable.'
                    if task.getRawEstimate() <= 0:
                        print >> out, 'Reason: no estimate (%s).' %  task.getRawEstimate()
                    if len(task.getAssignees()) == 0:
                        print >> out, 'Reason: no assignees.'
                    print >> out, 'Task name: %s' % task.title_or_id()
                    print >> out, 'URL: %s' % task.absolute_url()
                    print >> out, 'Staying in open state.'

    print >> out, '------------------'
    print >> out, 'Report on tasks migration:'
    print >> out, 'Migration gave %s errors.' % errors
    print >> out, 'Migration gave %s warnings.' % warnings
    return out.getvalue()

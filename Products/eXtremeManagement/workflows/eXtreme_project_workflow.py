# Generated by dumpDCWorkflow.py written by Sebastien Bigaret
# Original workflow id/title: eXtreme_project_workflow/Project Workflow [eXtreme Management]
# Date: 2005/10/22 21:38:24.403 GMT+2
#
# WARNING: this dumps does NOT contain any scripts you might have added to
# the workflow, IT IS YOUR RESPONSABILITY TO MAKE BACKUPS FOR THESE SCRIPTS.
#
# No script detected in this workflow
# 
"""
Programmatically creates a workflow type
"""
__version__ = "$Revision: 1.1.1.1 $"[11:-2]

from Products.CMFCore.WorkflowTool import addWorkflowFactory

from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition

def setupExtreme_project_workflow(wf):
    "..."
    wf.setProperties(title='Project Workflow [eXtreme Management]')

    for s in ['active', 'completed', 'private']:
        wf.states.addState(s)
    for t in ['deactivate', 'close', 'activate', 'reactivate']:
        wf.transitions.addTransition(t)
    for v in ['action', 'time', 'comments', 'actor', 'review_history']:
        wf.variables.addVariable(v)
    for l in ['reviewer_queue']:
        wf.worklists.addWorklist(l)
    for p in ('Access contents information', 'Modify portal content', 'View', 'List folder contents', 'Add Iteration Content', 'Add Story Content', 'Add portal content', 'Add Task Content', 'Add Booking Content', 'Delete objects', 'View management screens', 'Request review'):
        wf.addManagedPermission(p)
        

    ## Initial State
    wf.states.setInitialState('private')

    ## States initialization
    sdef = wf.states['active']
    sdef.setProperties(title="""Active""",
                       transitions=('close', 'deactivate'))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('List folder contents', 0, ['Customer', 'Employee', 'Manager', 'Owner'])
    sdef.setPermission('Add Iteration Content', 0, ['Customer', 'Employee', 'Manager'])
    sdef.setPermission('Add Story Content', 0, ['Customer', 'Employee', 'Manager'])
    sdef.setPermission('Add portal content', 1, ['Customer', 'Employee'])
    sdef.setPermission('Add Task Content', 0, ['Customer', 'Employee', 'Manager'])
    sdef.setPermission('Add Booking Content', 0, ['Employee', 'Manager'])
    sdef.setPermission('Delete objects', 1, ['Customer', 'Employee'])
    sdef.setPermission('View management screens', 1, ['Customer', 'Employee'])
    sdef.setPermission('Request review', 1, ['Customer'])

    sdef = wf.states['completed']
    sdef.setProperties(title="""Completed""",
                       transitions=('reactivate',))
    sdef.setPermission('Access contents information', 0, ['Customer', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, [])
    sdef.setPermission('View', 0, ['Customer', 'Manager', 'Owner'])
    sdef.setPermission('List folder contents', 0, [])
    sdef.setPermission('Add Iteration Content', 0, [])
    sdef.setPermission('Add Story Content', 0, [])
    sdef.setPermission('Add portal content', 0, [])
    sdef.setPermission('Add Task Content', 0, [])
    sdef.setPermission('Add Booking Content', 0, [])
    sdef.setPermission('Delete objects', 1, [])
    sdef.setPermission('View management screens', 1, [])
    sdef.setPermission('Request review', 1, [])

    sdef = wf.states['private']
    sdef.setProperties(title="""Private""",
                       transitions=('activate',))
    sdef.setPermission('Access contents information', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Modify portal content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('View', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('List folder contents', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Add Iteration Content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Add Story Content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Add portal content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Add Task Content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Add Booking Content', 0, ['Employee', 'Manager', 'Owner'])
    sdef.setPermission('Delete objects', 1, ['Employee'])
    sdef.setPermission('View management screens', 1, ['Employee'])
    sdef.setPermission('Request review', 1, [])


    ## Transitions initialization
    tdef = wf.transitions['deactivate']
    tdef.setProperties(title="""Deactivate""",
                       new_state_id="""private""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Deactivate""",
                       actbox_url="""%(content_url)s/content_hide_form""",
                       actbox_category="""workflow""",
                       props={'guard_roles': 'Owner; Manager'},
                       )

    tdef = wf.transitions['close']
    tdef.setProperties(title="""Close""",
                       new_state_id="""completed""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Close""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_roles': 'Owner; Manager'},
                       )

    tdef = wf.transitions['activate']
    tdef.setProperties(title="""Activate""",
                       new_state_id="""active""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Activate""",
                       actbox_url="""%(content_url)s/content_show_form""",
                       actbox_category="""workflow""",
                       props={'guard_roles': 'Owner; Manager'},
                       )

    tdef = wf.transitions['reactivate']
    tdef.setProperties(title="""Reactivate""",
                       new_state_id="""active""",
                       trigger_type=1,
                       script_name="""""",
                       after_script_name="""""",
                       actbox_name="""Reactivate""",
                       actbox_url="""""",
                       actbox_category="""workflow""",
                       props={'guard_roles': 'Owner; Manager'},
                       )

    ## State Variable
    wf.variables.setStateVar('review_state')

    ## Variables initialization
    vdef = wf.variables['action']
    vdef.setProperties(description="""The last transition""",
                       default_value="""""",
                       default_expr="""transition/getId|nothing""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['time']
    vdef.setProperties(description="""Time of the last transition""",
                       default_value="""""",
                       default_expr="""state_change/getDateTime""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['comments']
    vdef.setProperties(description="""Comments about the last transition""",
                       default_value="""""",
                       default_expr="""python:state_change.kwargs.get('comment', '')""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['actor']
    vdef.setProperties(description="""The ID of the user who performed the last transition""",
                       default_value="""""",
                       default_expr="""user/getId""",
                       for_catalog=0,
                       for_status=1,
                       update_always=1,
                       props=None)

    vdef = wf.variables['review_history']
    vdef.setProperties(description="""Provides access to workflow history""",
                       default_value="""""",
                       default_expr="""state_change/getHistory""",
                       for_catalog=0,
                       for_status=0,
                       update_always=0,
                       props={'guard_permissions': 'Request review; Review portal content'})

    ## Worklists Initialization
    ldef = wf.worklists['reviewer_queue']
    ldef.setProperties(description="""Reviewer tasks""",
                       actbox_name="""Pending (%(count)d)""",
                       actbox_url="""%(portal_url)s/search?review_state=pending""",
                       actbox_category="""global""",
                       props={'guard_permissions': 'Review portal content', 'var_match_review_state': 'pending'})


def createExtreme_project_workflow(id):
    "..."
    ob = DCWorkflowDefinition(id)
    setupExtreme_project_workflow(ob)
    return ob

addWorkflowFactory(createExtreme_project_workflow,
                   id='eXtreme_project_workflow',
                   title='Project Workflow [eXtreme Management]')
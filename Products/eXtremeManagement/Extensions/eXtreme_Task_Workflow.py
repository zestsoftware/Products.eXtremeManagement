# File: eXtremeManagement.py
#
# Copyright (c) 2006 by Zest software
# Generator: ArchGenXML Version 1.4.1 svn/devel
#            http://plone.org/products/archgenxml
#
# GNU General Public License (GPL)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA
# 02110-1301, USA.
#

__author__ = """Ahmad Hadi <a.hadi@zestsoftware.nl>, Maurits van Rees
<m.van.rees@zestsoftware.nl>"""
__docformat__ = 'plaintext'


from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.eXtremeManagement.config import *

##code-section create-workflow-module-header #fill in your manual code here
##/code-section create-workflow-module-header


productname = 'eXtremeManagement'

def setupeXtreme_Task_Workflow(self, workflow):
    """Define the eXtreme_Task_Workflow workflow.
    """
    # Add additional roles to portal
    portal = getToolByName(self,'portal_url').getPortalObject()
    data = list(portal.__ac_roles__)
    for role in ['Employee', 'Customer']:
        if not role in data:
            data.append(role)
    portal.__ac_roles__ = tuple(data)

    workflow.setProperties(title='eXtreme_Task_Workflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['to-do', 'completed', 'open']:
        workflow.states.addState(s)

    for t in ['deactivate', 'activate', 'complete', 'reactivate']:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    workflow.addManagedPermission('Access contents information')
    workflow.addManagedPermission('Modify portal content')
    workflow.addManagedPermission('View')
    workflow.addManagedPermission('Change portal events')
    workflow.addManagedPermission('eXtremeManagement: Add Booking')

    for l in []:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('open')

    ## States initialization

    stateDef = workflow.states['to-do']
    stateDef.setProperties(title="""To-do""",
                           transitions=['complete', 'deactivate'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Employee', 'Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Employee', 'Manager', 'Owner'])
    stateDef.setPermission('eXtremeManagement: Add Booking',
                           0,
                           ['Employee', 'Manager'])

    stateDef = workflow.states['completed']
    stateDef.setProperties(title="""Completed""",
                           transitions=['reactivate'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Employee', 'Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Employee', 'Manager', 'Owner'])
    stateDef.setPermission('eXtremeManagement: Add Booking',
                           0,
                           [])

    stateDef = workflow.states['open']
    stateDef.setProperties(title="""New""",
                           transitions=['activate'])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Employee', 'Manager', 'Owner'])
    stateDef.setPermission('View',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Change portal events',
                           0,
                           ['Employee', 'Manager', 'Owner'])
    stateDef.setPermission('eXtremeManagement: Add Booking',
                           0,
                           ['Employee', 'Manager'])

    ## Transitions initialization

    transitionDef = workflow.transitions['deactivate']
    transitionDef.setProperties(title="""deactivate""",
                                new_state_id="""open""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""deactivate""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager'},
                                )

    transitionDef = workflow.transitions['activate']
    transitionDef.setProperties(title="""activate""",
                                new_state_id="""to-do""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""activate""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_expr': 'here/startable', 'guard_roles': 'Manager;Employee'},
                                )

    ## Creation of workflow scripts
    for wf_scriptname in ['notify_completed', 'tryToCompleteStory']:
        if not wf_scriptname in workflow.scripts.objectIds():
            workflow.scripts._setObject(wf_scriptname,
                ExternalMethod(wf_scriptname, wf_scriptname,
                productname + '.eXtreme_Task_Workflow_scripts',
                wf_scriptname))

    transitionDef = workflow.transitions['complete']
    transitionDef.setProperties(title="""Mark as completed""",
                                new_state_id="""completed""",
                                trigger_type=1,
                                script_name="""notify_completed""",
                                after_script_name="""tryToCompleteStory""",
                                actbox_name="""Mark as completed""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Employee;Manager'},
                                )

    transitionDef = workflow.transitions['reactivate']
    transitionDef.setProperties(title="""Reactivate this task""",
                                new_state_id="""to-do""",
                                trigger_type=1,
                                script_name="""""",
                                after_script_name="""""",
                                actbox_name="""Reactivate this task""",
                                actbox_url="""""",
                                actbox_category="""workflow""",
                                props={'guard_roles': 'Manager;Employee'},
                                )

    ## State Variable
    workflow.variables.setStateVar('review_state')

    ## Variables initialization
    variableDef = workflow.variables['review_history']
    variableDef.setProperties(description="""Provides access to workflow history""",
                              default_value="""""",
                              default_expr="""state_change/getHistory""",
                              for_catalog=0,
                              for_status=0,
                              update_always=0,
                              props={'guard_permissions': 'Request review; Review portal content'})

    variableDef = workflow.variables['comments']
    variableDef.setProperties(description="""Comments about the last transition""",
                              default_value="""""",
                              default_expr="""python:state_change.kwargs.get('comment', '')""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['time']
    variableDef.setProperties(description="""Time of the last transition""",
                              default_value="""""",
                              default_expr="""state_change/getDateTime""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['actor']
    variableDef.setProperties(description="""The ID of the user who performed the last transition""",
                              default_value="""""",
                              default_expr="""user/getId""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    variableDef = workflow.variables['action']
    variableDef.setProperties(description="""The last transition""",
                              default_value="""""",
                              default_expr="""transition/getId|nothing""",
                              for_catalog=0,
                              for_status=1,
                              update_always=1,
                              props=None)

    ## Worklists Initialization


    # WARNING: below protected section is deprecated.
    # Add a tagged value 'worklist' with the worklist name to your state(s) instead.

    ##code-section create-workflow-setup-method-footer #fill in your manual code here
    ##/code-section create-workflow-setup-method-footer



def createeXtreme_Task_Workflow(self, id):
    """Create the workflow for eXtremeManagement.
    """

    ob = DCWorkflowDefinition(id)
    setupeXtreme_Task_Workflow(self, ob)
    return ob

addWorkflowFactory(createeXtreme_Task_Workflow,
                   id='eXtreme_Task_Workflow',
                   title='eXtreme_Task_Workflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer


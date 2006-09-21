# -*- coding: utf-8 -*-
#
# File: eXtremeManagement.py
#
# Copyright (c) 2006 by Zest software, Lovely Systems
# Generator: ArchGenXML Version 1.5.1-svn
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
<m.van.rees@zestsoftware.nl>, Jodok Batlogg <jodok.batlogg@lovelysystems.com>"""
__docformat__ = 'plaintext'


from Products.CMFCore.utils import getToolByName
from Products.CMFCore.WorkflowTool import addWorkflowFactory
from Products.DCWorkflow.DCWorkflow import DCWorkflowDefinition
from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.eXtremeManagement.config import *

##code-section create-workflow-module-header #fill in your manual code here
##/code-section create-workflow-module-header


productname = 'eXtremeManagement'

def setupeXtreme_Customer_Workflow(self, workflow):
    """Define the eXtreme_Customer_Workflow workflow.
    """
    # Add additional roles to portal
    portal = getToolByName(self,'portal_url').getPortalObject()
    data = list(portal.__ac_roles__)
    for role in ['Customer', 'Employee']:
        if not role in data:
            data.append(role)
    portal.__ac_roles__ = tuple(data)

    workflow.setProperties(title='eXtreme_Customer_Workflow')

    ##code-section create-workflow-setup-method-header #fill in your manual code here
    ##/code-section create-workflow-setup-method-header


    for s in ['active']:
        workflow.states.addState(s)

    for t in []:
        workflow.transitions.addTransition(t)

    for v in ['review_history', 'comments', 'time', 'actor', 'action']:
        workflow.variables.addVariable(v)

    workflow.addManagedPermission('Access contents information')
    workflow.addManagedPermission('Add portal content')
    workflow.addManagedPermission('Delete objects')
    workflow.addManagedPermission('List folder contents')
    workflow.addManagedPermission('Modify portal content')
    workflow.addManagedPermission('Request review')
    workflow.addManagedPermission('View')
    workflow.addManagedPermission('View management screens')

    for l in []:
        if not l in workflow.worklists.objectValues():
            workflow.worklists.addWorklist(l)

    ## Initial State

    workflow.states.setInitialState('active')

    ## States initialization

    stateDef = workflow.states['active']
    stateDef.setProperties(title="""Active""",
                           transitions=[])
    stateDef.setPermission('Access contents information',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Add portal content',
                           1,
                           ['Customer', 'Employee'])
    stateDef.setPermission('Delete objects',
                           1,
                           ['Customer', 'Employee'])
    stateDef.setPermission('List folder contents',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('Modify portal content',
                           0,
                           ['Employee', 'Manager'])
    stateDef.setPermission('Request review',
                           1,
                           ['Customer'])
    stateDef.setPermission('View',
                           0,
                           ['Customer', 'Employee', 'Manager', 'Owner'])
    stateDef.setPermission('View management screens',
                           1,
                           ['Customer', 'Employee'])

    ## Transitions initialization

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



def createeXtreme_Customer_Workflow(self, id):
    """Create the workflow for eXtremeManagement.
    """

    ob = DCWorkflowDefinition(id)
    setupeXtreme_Customer_Workflow(self, ob)
    return ob

addWorkflowFactory(createeXtreme_Customer_Workflow,
                   id='eXtreme_Customer_Workflow',
                   title='eXtreme_Customer_Workflow')

##code-section create-workflow-module-footer #fill in your manual code here
##/code-section create-workflow-module-footer

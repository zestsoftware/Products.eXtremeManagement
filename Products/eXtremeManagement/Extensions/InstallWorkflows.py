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
from Products.ExternalMethod.ExternalMethod import ExternalMethod

def installWorkflows(self, package, out):
    """Install the custom workflows for this product."""

    productname = 'eXtremeManagement'
    workflowTool = getToolByName(self, 'portal_workflow')

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'eXtreme_Project_Workflow',
                         'createeXtreme_Project_Workflow')
    workflow = ourProductWorkflow(self, 'eXtreme_Project_Workflow')
    workflowTool._setObject('eXtreme_Project_Workflow', workflow)
    workflowTool.setChainForPortalTypes(['Project'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'eXtreme_Iteration_Workflow',
                         'createeXtreme_Iteration_Workflow')
    workflow = ourProductWorkflow(self, 'eXtreme_Iteration_Workflow')
    workflowTool._setObject('eXtreme_Iteration_Workflow', workflow)
    workflowTool.setChainForPortalTypes(['Iteration'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'eXtreme_Story_Workflow',
                         'createeXtreme_Story_Workflow')
    workflow = ourProductWorkflow(self, 'eXtreme_Story_Workflow')
    workflowTool._setObject('eXtreme_Story_Workflow', workflow)
    workflowTool.setChainForPortalTypes(['Story'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'eXtreme_Task_Workflow',
                         'createeXtreme_Task_Workflow')
    workflow = ourProductWorkflow(self, 'eXtreme_Task_Workflow')
    workflowTool._setObject('eXtreme_Task_Workflow', workflow)
    workflowTool.setChainForPortalTypes(['Task'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'eXtreme_Default_Workflow',
                         'createeXtreme_Default_Workflow')
    workflow = ourProductWorkflow(self, 'eXtreme_Default_Workflow')
    workflowTool._setObject('eXtreme_Default_Workflow', workflow)
    workflowTool.setChainForPortalTypes(['WorkflowStub', 'ProjectMember', 'Customer'], workflow.getId())

    ourProductWorkflow = ExternalMethod('temp', 'temp',
                         productname+'.'+'eXtreme_Booking_Workflow',
                         'createeXtreme_Booking_Workflow')
    workflow = ourProductWorkflow(self, 'eXtreme_Booking_Workflow')
    workflowTool._setObject('eXtreme_Booking_Workflow', workflow)
    workflowTool.setChainForPortalTypes(['Booking'], workflow.getId())

    return workflowTool

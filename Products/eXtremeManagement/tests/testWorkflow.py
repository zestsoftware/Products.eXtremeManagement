# File: testWorkflow.py
#
# Copyright (c) 2006 by Zest software
# Generator: ArchGenXML 
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

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

##code-section module-header #fill in your manual code here
##/code-section module-header

#
# Test-cases for class(es) 
#

from Testing import ZopeTestCase
from Products.eXtremeManagement.tests.eXtremeManagementTestCase import eXtremeManagementTestCase

# Import the tested classes

##code-section module-beforeclass #fill in your manual code here
from Products.CMFCore.WorkflowCore import WorkflowException
from Products.PloneTestCase.setup import default_user
##/code-section module-beforeclass


class testWorkflow(eXtremeManagementTestCase):
    """ test-cases for class(es) 
    """

    ##code-section class-header_testWorkflow #fill in your manual code here
    ##/code-section class-header_testWorkflow

    def afterSetUp(self):
        self.catalog = self.portal.portal_catalog
        self.workflow = self.portal.portal_workflow
        self.userfolder = self.portal.acl_users
        self.default_user = default_user

        #self.userfolder._doAddUser('initial', 'secret', ['Manager'], [])
        self.userfolder._doAddUser('member', 'secret', ['Member'], [])
        self.userfolder._doAddUser('reviewer', 'secret', ['Reviewer'], [])
        self.userfolder._doAddUser('manager', 'secret', ['Manager'], [])
        self.userfolder._doAddUser('employee', 'secret', ['Employee'], [])
        self.userfolder._doAddUser('customer', 'secret', ['Customer'], [])

        #self.login('initial')
        self.login('manager')
        # Create a projectfolder in the portal root
        self.portal.invokeFactory('ProjectFolder', id='projects')
        self.projects = self.folder.projects

        self.projects.invokeFactory('Project', id='project')
        self.project = self.projects.project
        self.project.manage_addLocalRoles('customer',['Customer'])

        self.project.invokeFactory('Iteration', id='iteration')
        self.iteration = self.project.iteration

        # Create Story in iteration
        self.iteration.invokeFactory('Story', id='story')
        self.story = self.iteration.story

        # Create Story directly in project. At the moment this is
        # allowed, but this may change in the future.
        self.project.invokeFactory('Story', id='projectstory')
        self.projectstory = self.project.projectstory

        self.login('employee')
        self.story.invokeFactory('Task', id='task')
        self.task = self.story.task

        self.task.invokeFactory('Booking', id='booking')
        self.booking = self.task.booking
        self.main_objects = [self.portal, self.projects, self.project,
                             self.iteration, self.story, self.task,
                             self.booking]
        self.logout()
        self.login(self.default_user)

    # Manually created methods
    def tryForbiddenTransition(self, ctObject, originalState,
                               workflowTransition):
        """
        Try to execute a transaction that you are not allowed to do
        ctObject = Content Type object to perform the transition on
        originalState = currect state of the object
        workflowTransition = transition to perform
        """
        self.assertEqual(self.workflow.getInfoFor(ctObject, 'review_state'),
                         originalState)
        self.assertRaises(WorkflowException,
                          self.workflow.doActionFor, ctObject, workflowTransition)

    def testProjectTransitions(self):
        """Test transitions of the Project Content Type
        """
        # Manager (same as Owner here) can transition a project:
        # private -> active -> completed -> active -> private
        self.login('manager')
        self.tryAllowedTransition(self.project, 'project',
                                  'private', 'activate', 'active')
        self.tryAllowedTransition(self.project, 'project',
                                  'active', 'close', 'completed')
        self.tryAllowedTransition(self.project, 'project',
                                  'completed', 'reactivate', 'active')
        self.tryAllowedTransition(self.project, 'project',
                                  'active', 'deactivate', 'private')

        # Try some forbidden transactions
        self.login('reviewer')
        self.tryForbiddenTransition(self.project, 'private', 'activate')
        self.login('employee')
        self.tryForbiddenTransition(self.project, 'private', 'activate')
        self.login('customer')
        self.tryForbiddenTransition(self.project, 'private', 'activate')
        
        # Try some transactions that don't belong to the current state
        self.login('manager')
        self.tryForbiddenTransition(self.project, 'private', 'reactivate')
        self.tryAllowedTransition(self.project, 'project',
                                  'private', 'activate', 'active')
        self.tryForbiddenTransition(self.project, 'active', 'reactivate')
        self.login('employee')
        self.tryForbiddenTransition(self.project, 'active', 'close')
        self.login('customer')
        self.tryForbiddenTransition(self.project, 'active', 'close')

    def testStoryTransitions(self):
        """Test transitions of the Story Content Type
        """

        #self.login('customer')
        #self.login('manager')
        self.setRoles(['Manager'])
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'submit', 'pending')
        self.tryAllowedTransition(self.story, 'story',
                                  'pending', 'retract', 'draft')
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'estimate', 'estimated')
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'refactor', 'draft')

        #self.printGlobalRolesUser(self.default_user)
        # Not quite working:
        #self.setPermissions(['Add portal content'])


        # Some tests to see how I can get information about users:

        """
        for object in self.main_objects:
            self.printLocalPermissions(object, self.default_user)
        for role in ['Member','Authenticated','Employee','Customer','Reviewer','Owner']:
            print '%s portal roles:' % role
            print self.getPermissionsOfRole(self.portal, role)
        for user in self.userfolder.getUserIds():
            print '##############################'
            print user + ':'
            print 'global roles:'
            self.printGlobalRolesUser(user)

            for object in self.main_objects:
                self.printLocalPermissions(object, user)

        self.loginAsPortalOwner()
        for object in self.main_objects:
            print object.title_or_id()
            print 'getAllLocalRoles:'
            print self.userfolder.getAllLocalRoles(object)
            print 'getLocalRolesForDisplay:'
            print self.userfolder.getLocalRolesForDisplay(object)
        """


        self.setRoles(['Employee'])
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'estimate', 'estimated')
        self.tryAllowedTransition(self.story, 'story',
                                  'estimated', 'refactor', 'draft')

        self.setRoles(['Manager'])
        self.tryAllowedTransition(self.project, 'project',
                                  'private', 'activate', 'active')
        self.setRoles(['Customer'])
        # But default_user does NOT have the LOCAL role Customer.
        #self.setPermissions(['Request review'])
        #self.story.manage_addLocalRoles(self.default_user,['Customer'])
        #self.printGlobalRolesUser(self.default_user)
        for object in self.main_objects:
            self.printLocalPermissions(object, self.default_user)
        self.tryAllowedTransition(self.story, 'story',
                                  'draft', 'submit', 'pending')
        self.tryAllowedTransition(self.story, 'story',
                                  'pending', 'retract', 'draft')

    def printLocalPermissions(self, object, userid):
        print 'Local roles on %s:' % object.title_or_id()
        roles = object.get_local_roles_for_userid(userid)
        for role in roles:
            print '    role %s:' % role
            print '    with explicit permissions:'
            print self.getPermissionsOfRole(object, role)

    def testInitialStates(self):
        self.assertEqual(self.workflow.getInfoFor(self.projects, 'review_state'), 'visible')
        self.assertEqual(self.workflow.getInfoFor(self.project, 'review_state'), 'private')
        self.assertEqual(self.workflow.getInfoFor(self.iteration, 'review_state'), 'new')
        self.assertEqual(self.workflow.getInfoFor(self.story, 'review_state'), 'draft')
        self.assertEqual(self.workflow.getInfoFor(self.projectstory, 'review_state'), 'draft')
        self.assertEqual(self.workflow.getInfoFor(self.task, 'review_state'), 'open')
        self.assertEqual(self.workflow.getInfoFor(self.booking, 'review_state'), 'booking')

    def printGlobalRolesUser(self, userid):
        roles = self.userfolder.getUserById(self.default_user).getRoles()
        for role in roles:
            print '    role %s:' % role
            if role == 'Manager':
                print 'A Manager can do anything.'
            else:
                print self.getPermissionsOfRole(self.portal, role)

    def tryAllowedTransition(self, ctObject, ctId, originalState,
                       workflowTransition, newState):
        """
        Test a transition.
        ctObject = Content Type object to perform the transition on
        ctId = id of object in the plone portal
        originalState = currect state of the object
        workflowTransition = transition to perform
        newState = desired new state after the transition
        """
        self.assertEqual(self.workflow.getInfoFor(ctObject, 'review_state'),
                         originalState)
        self.workflow.doActionFor(ctObject, workflowTransition)
        self.assertEqual(self.workflow.getInfoFor(ctObject, 'review_state'),
                         newState)
        self.failUnless(self.catalog(id=ctId, review_state=newState))

    def testIterationTransitions(self):
        """Test transitions of the Iteration Content Type
        """

        # Manager can do all transitions on an iteration:
        self.login('manager')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'new', 'accept', 'in-progress')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'in-progress', 'complete', 'completed')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'completed', 'reactivate', 'in-progress')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'in-progress', 'retract', 'new')

        # Try some forbidden transactions
        self.login('customer')
        self.tryForbiddenTransition(self.iteration, 'new', 'accept')

        # Employee can only accept and complete an iteration
        self.login('employee')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'new', 'accept', 'in-progress')
        self.tryForbiddenTransition(self.iteration, 'in-progress', 'retract')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'in-progress', 'complete', 'completed')
        self.tryForbiddenTransition(self.iteration, 'completed', 'reactivate')

        # Only a Manager can do an invoice
        self.tryForbiddenTransition(self.iteration, 'completed', 'invoice')
        self.login('customer')
        self.tryForbiddenTransition(self.iteration, 'completed', 'invoice')
        self.login('manager')
        self.tryAllowedTransition(self.iteration, 'iteration',
                                  'completed', 'invoice', 'invoiced')

        
        # Try some transactions that don't belong to the current state
        self.tryForbiddenTransition(self.iteration, 'invoiced', 'reactivate')

    def getPermissionsOfRole(self, object, role):
        perms = object.permissionsOfRole(role)
        return [p['name'] for p in perms if p['selected']]

    def getPermissionSettings(self, object, permission):
        permission_settings = object.permission_settings(permission)
        if permission_settings == []:
            return []
        roles = permission_settings[0]['roles']
        return [role['name'] for role in roles if role['checked']]



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(testWorkflow))
    return suite

##code-section module-footer #fill in your manual code here
##/code-section module-footer

if __name__ == '__main__':
    framework()



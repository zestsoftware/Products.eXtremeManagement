# AUTHORS: Ahmad Hadi

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal
from StringIO import StringIO

from Products.eXtremeManagement.config import PROJECTNAME, GLOBALS
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.workflows import eXtreme_iteration_workflow, \
                                                 eXtreme_story_workflow, eXtreme_task_workflow
from Products.eXtremeManagement.permissions import eXtremeManagementRols 

from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFDefault.PropertiesTool import PropertiesTool


def configureRoles(portal):
    # add new roles
    defined_roles = getattr(portal, '__ac_roles__', ())
    if defined_roles is None:
        defined_roles = []
    else:
        defined_roles = list(defined_roles)
    
    defined_roles = Set(defined_roles)
 
    for role in eXtremeManagementRoles:
        defined_roles.add(role)

    portal.__ac_roles__ = tuple(defined_roles)

#    for role, permissions in RolePermissionMap.items():
#        existing_permissions = portal.permissionsOfRole(role)
#        permissions = Set(permissions)
#	for perm in existing_permissions:
#            if perm['selected']:
#                permissions.add( perm['name'] )
#	portal.manage_role(role, permissions)

def configureUserActions(portal):
    # add an action to the persnal bar for project management
    actionTool = getToolByName(portal, 'portal_membership', None)
    actionTool_actions = actionTool._cloneActions()
    actionDefined=0
    for a in actionTool_actions: 
        if a.id in ['eXtremeProjectMangement',]:
            a.visible = 1
            actionDefined = 1
        actionTool._actions = actionTool_actions
    if actionDefined == 0:
        actionTool.addAction('eXtremeProjectManagement', 
                             'eXtreme Project Mangement',
                             'string:${portal_url}/prefs_project_management',
                             '',
                             'ManagePortal',
                             'user'
                            )

def configureConfiglets(portal):
    # add configlets to portal control panel
    configTool = getToolByName(portal, 'portal_controlpanel', None)
    if configTool:
        for conf in configlets:
            configTool.registerConfiglet(**conf)
            #out.write('Added configlet %s\n' % conf['id'])

def configureWorkflow(portal):
    # set the workflow for the new content types (Iteration, Story, Task)
    # We need to do the updateRoleMappings only once after all workflows have been set
    # because otherwise the empty one are reseted to (Default)
    # clear the workflow for migration tool

    wf_tool = getToolByName(portal, 'portal_workflow')
    wf_tool.setChainForPortalTypes(('Iteration',), 'eXtreme_iteration_workflow')
    wf_tool.setChainForPortalTypes(('Story',), 'eXtreme_story_workflow')
    wf_tool.setChainForPortalTypes(('Task',), 'eXtreme_task_workflow')
    wf_tool.updateRoleMappings()

    eiwf = 'eXtreme_iteration_workflow'
    #eXtreme_iteration_workflow.createEXtreme_iteration_workflow(eiwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not eiwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_iteration_workflow (eXtreme Iteration Workflow)', eiwf)
    wf_tool.setChainForPortalTypes( ('Iteration',), eiwf)

    eswf = 'eXtreme_story_workflow'
    #eXtreme_story_workflow.createEXtreme_story_workflow(eswf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not eswf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_story_workflow (eXtreme Story Workflow)', eswf)
    wf_tool.setChainForPortalTypes( ('Story',), eswf)

    etwf = 'eXtreme_task_workflow'
    #eXtreme_task_workflow.createEXtreme_task_workflow(etwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not etwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_task_workflow (eXtreme Task Workflow)', etwf)
    wf_tool.setChainForPortalTypes( ('Task',), etwf)


#def setupProps(portal):
#    # Add eXtreme Props
#    if not hasattr(portal.portal_properties, 'extreme_properties'):
#        portal.portal_properties.addPropertySheet('extreme_properties', 'eXtreme Properties')
#        props = portal.portal_properties.extreme_properties
#        props._setProperty('hours', ['01', '02', '03', '04', '05', '06', '07', 
#                                     '08', '09', '10', '11', '12', '13', '14', '15'], 'lines')
#        props._setProperty('minutes', ['0', '15', '30', '45'], 'lines')


def setupSkin(portal):
    # Set up the skins
    _dirs = ('eXtremeManagement', )
    sk_tool = getToolByName(portal, 'portal_skins')
    path = [elem.strip() for elem in sk_tool.getSkinPath('Plone Default').split(',')]

    for d in _dirs:
        try: path.insert(path.index('custom')+1, d)
        except ValueError: path.append(d)

    path = ','.join(path)
    sk_tool.addSkinSelection('eXtremeManagement', path)
    if not 'eXtremeManagement' in  portal.portal_skins.objectIds():
        addDirectoryViews(sk_tool, 'skins', globals())
    # set default skin
    sk_tool.default_skin = 'eXtremeManagement'


def install(self):
    out = StringIO()
    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)
   
    print >> out, "Customize the portal"
    setupSkin(self)
 
#    print >> out, "Configuring new roles"
#    configureRoles(self)

    print >> out, "Configuring workflows"
    configureWorkflow(self)

    print >> out, "Registering user actions"
    configureUserActions(self)
 
    return out.getvalue()

def uninstall(self):
    out = StringIO()

    # remove the configlets from the portal control panel
    #configTool = getToolByName(self, 'portal_controlpanel', None)
    #if configTool:
    #    for conf in configlets:
    #        configTool.unregisterConfiglet(conf['id'])
    #        out.write('Removed configlet %s\n' % conf['id'])

    return out.getvalue()

 

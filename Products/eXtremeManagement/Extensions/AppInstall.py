# AUTHORS: Ahmad Hadi (ahadi@zestsoftware.nl)

from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFDefault.PropertiesTool import PropertiesTool
from StringIO import StringIO
from sets import Set

#from Products.eXtremeManagement.config import PROJECTNAME, GLOBALS
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.workflows import *
from Products.eXtremeManagement.permissions import * 


def configureRoles(portal):
    defined_roles = getattr( portal, '__ac_roles__', ())

    if defined_roles is None:
        defined_roles = []
    else:
        defined_roles = list(defined_roles)
    defined_roles = Set(defined_roles)

    for role in eXtremeManagementRoles:
        defined_roles.add(role)
    portal.__ac_roles__ = tuple(defined_roles)


def configurePortalProps(portal):
    # customize portal props (slots)
    left_slots = portal.getProperty('left_slots', None)
    newSlot = ('here/portlet_tasks/macros/portlet', 
               'here/portlet_stories/macros/portlet',)
    for a in newSlot:
        if a not in left_slots:
            portal._updateProperty('left_slots', tuple(left_slots) + tuple(newSlot)) 

    # update navtree_props
    props_tool = getToolByName(portal, 'portal_properties')
    rolesSeeUnpublishedContent = props_tool.navtree_properties.getProperty('rolesSeeUnpublishedContent', None)
    roles = ('Customer',)
    for role in roles:
        if role not in rolesSeeUnpublishedContent:
            props_tool.navtree_properties._updateProperty('rolesSeeUnpublishedContent', 
                                                          tuple(rolesSeeUnpublishedContent) + tuple(roles))
    metaTypesNotToList = props_tool.navtree_properties.getProperty('metaTypesNotToList', None)
    ptypes = ('ProjectMember','Booking','Task')
    for ptype in ptypes:
        if ptype not in metaTypesNotToList:
            props_tool.navtree_properties._updateProperty('metaTypesNotToList', 
                                                          tuple(metaTypesNotToList) + ptypes)

def configureWorkflow(portal):
    # set the workflow for the new content types (Iteration, Story, Task)
    # We need to do the updateRoleMappings only once after all workflows have been set
    # because otherwise the empty one are reseted to (Default)
    # clear the workflow for migration tool

    wf_tool = getToolByName(portal, 'portal_workflow')
    wf_tool.setChainForPortalTypes(('CustomerFolder', 'ProjectFolder'), 'folder_workflow')
    wf_tool.updateRoleMappings()

    eiwf = 'eXtreme_iteration_workflow'
    eXtreme_iteration_workflow.createExtreme_iteration_workflow(eiwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not eiwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_iteration_workflow (eXtreme Iteration Workflow)', eiwf)
    wf_tool.setChainForPortalTypes( ('Iteration',), eiwf)

    eswf = 'eXtreme_story_workflow'
    eXtreme_story_workflow.createExtreme_story_workflow(eswf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not eswf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_story_workflow (eXtreme Story Workflow)', eswf)
    wf_tool.setChainForPortalTypes( ('Story',), eswf)

    etwf = 'eXtreme_task_workflow'
    eXtreme_task_workflow.createExtreme_task_workflow(etwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not etwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_task_workflow (eXtreme Task Workflow)', etwf)
    wf_tool.setChainForPortalTypes( ('Task',), etwf)

    ebwf = 'eXtreme_booking_workflow'
    eXtreme_booking_workflow.createExtreme_booking_workflow(ebwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not ebwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_booking_workflow (eXtreme Booking Workflow)', ebwf)
    wf_tool.setChainForPortalTypes( ('Booking',), ebwf)

    edwf = 'eXtreme_default_workflow'
    eXtreme_default_workflow.createExtreme_default_workflow(edwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not edwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_default_workflow (eXtreme Default Workflow)', edwf)
    wf_tool.setChainForPortalTypes( ('Customer', 'ProjectMember'), edwf)

    epwf = 'eXtreme_project_workflow'
    eXtreme_project_workflow.createExtreme_project_workflow(epwf)
    wf_tool = getToolByName(portal, 'portal_workflow')
    if not epwf in wf_tool.objectIds():
        wf_tool.manage_addWorkflow('eXtreme_project_workflow (Project Workflow [eXtreme Management])', epwf)
    wf_tool.setChainForPortalTypes( ('Project',), epwf)


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


def addFolders(portal):
    wf = getToolByName(portal, 'portal_workflow')
    if not 'customers' in portal.objectIds():
        portal.invokeFactory(type_name='CustomerFolder', id='customers', title='Customers')
        types_tool = getToolByName(portal, 'portal_types')
        types_tool.CustomerFolder._updateProperty('global_allow', 0)

    if not 'projects' in portal.objectIds():
        portal.invokeFactory(type_name='ProjectFolder', id='projects', title='Projects')
        types_tool = getToolByName(portal, 'portal_types')
        types_tool.ProjectFolder._updateProperty('global_allow', 0)


def install(self):
    out = StringIO()
    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)
   
    print >> out, "Customize the portal"
    setupSkin(self)
 
    print >> out, "Configuring new roles"
    configureRoles(self)

    print >> out, "Customizing portal properties"
    configurePortalProps(self)
 
    print >> out, "Configuring workflows"
    configureWorkflow(self)

    # Turned off for now.
    #print >> out, "Adding default folders"
    #addFolders(self)

    return out.getvalue()

def uninstall(self):
    out = StringIO()


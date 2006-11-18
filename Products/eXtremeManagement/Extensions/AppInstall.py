# AUTHORS: Ahmad Hadi (ahadi@zestsoftware.nl),
# Maurits van Rees (m.van.rees@zestsoftware.nl)


from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ManagePortal
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFDefault.PropertiesTool import PropertiesTool
from StringIO import StringIO
from sets import Set

from Products.eXtremeManagement.config import *


def configurePortalProps(portal):
    # customize portal props (slots)
    left_slots = portal.getProperty('left_slots', None)
    newSlots = ()
    for slot in XM_LEFT_SLOTS:
        if slot not in left_slots:
            newSlots = newSlots + (slot,)
    portal._updateProperty('left_slots', tuple(left_slots) + newSlots) 

    right_slots = portal.getProperty('right_slots', None)
    newSlots = ()
    for slot in XM_RIGHT_SLOTS:
        if slot not in right_slots:
            newSlots = newSlots + (slot,)
    portal._updateProperty('right_slots', tuple(right_slots) + newSlots) 

    # update navtree_props
    props_tool = getToolByName(portal, 'portal_properties')
    if props_tool.navtree_properties.hasProperty('rolesSeeUnpublishedContent'):
        rolesSeeUnpublishedContent = props_tool.navtree_properties.getProperty(
            'rolesSeeUnpublishedContent')
        roles = ('Customer',)
        newroles = [role for role in roles if role not in rolesSeeUnpublishedContent]

        props_tool.navtree_properties._updateProperty(
            'rolesSeeUnpublishedContent',
            tuple(rolesSeeUnpublishedContent) + tuple(newroles))

    if props_tool.navtree_properties.hasProperty('metaTypesNotToList'):
        metaTypesNotToList = props_tool.navtree_properties.getProperty(
            'metaTypesNotToList')
        ptypes = ('ProjectMember','Booking','Task')
        newptypes = [ptype for ptype in ptypes if ptype not in metaTypesNotToList]
        props_tool.navtree_properties._updateProperty(
            'metaTypesNotToList',
            tuple(metaTypesNotToList) + tuple(ptypes))


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

def disableJoinLink(portal):
    """- Only manager is allowed to add members.
    """
    portal.manage_permission('Add portal member', ['Manager'], 0)


def _migrateSchema(self, contentType):
    at = getToolByName(self, 'archetype_tool')
    class dummy:
        form = {}
    dummyRequest = dummy()
    dummy.form[contentType] = 1
    at.manage_updateSchema(update_all=1,
                           REQUEST=dummyRequest)

def _migrateProjectSchema(self):
    _migrateSchema(self, 'eXtremeManagement.Iteration')

def _migrateIterationSchema(self):
    _migrateSchema(self, 'eXtremeManagement.Iteration')

def _migrateStorySchema(self):
    _migrateSchema(self, 'eXtremeManagement.Story')

def _migrateTaskSchema(self):
    """
    Add a property to the portal so that other parts now that there is
    a schema update going on for the Tasks.  Main reason: if this is
    True, then _do not_ send an email for every Task that is getting
    assigned.  See Task.setAssigned()
    """
    propertyName = 'xm_task_schema_updating'
    self.manage_addProperty(propertyName, True, 'boolean')
    _migrateSchema(self, 'eXtremeManagement.Task')
    self.manage_delProperties((propertyName,))

def _migrateBookingSchema(self):
    _migrateSchema(self, 'eXtremeManagement.Booking')


def migrate_stories(portal, out):
    print >> out, "Updating Story schema."
    _migrateStorySchema(portal)
    print >> out, "Done."

def migrate_tasks(portal, out):
    print >> out, "Updating Task schema."
    _migrateTaskSchema(portal)
    print >> out, "Done."


def migrate_bookings(portal, out):
    print >> out, "Updating Booking schema."
    _migrateBookingSchema(portal)
    print >> out, "Migration of bookings completed."

def migrate_ct(portal, out):
    """

    """
    migrate_stories(portal, out)
    migrate_tasks(portal, out)

def configureKupu(portal):
    try:
        kupuTool = getToolByName(portal, 'kupu_library_tool')
    except AttributeError:
        # kupu is not installed apparently, so no need to configure it
        return
    linkable = list(kupuTool.getPortalTypesForResourceType('linkable'))
    #mediaobject = list(kupuTool.getPortalTypesForResourceType('mediaobject'))
    collection = list(kupuTool.getPortalTypesForResourceType('collection'))

    for type in OUR_LINKABLE_TYPES:
        if type not in linkable:
            linkable.append(type)

    for type in OUR_COLLECTION_TYPES:
        if type not in collection:
            collection.append(type)

    # kupu_library_tool has an idiotic interface, basically written purely to
    # work with its configuration page. :-(
    kupuTool.updateResourceTypes(({'resource_type' : 'linkable',
                                   'old_type'      : 'linkable',
                                   'portal_types'  :  linkable},
                                  {'resource_type' : 'collection',
                                   'old_type'      : 'collection',
                                   'portal_types'  :  collection},))

def addOurRoles(portal):
    """Add our extra roles to Plone.
    """

    defined_roles = getattr(portal, '__acl_roles__', ())
    if HAS_PAS:
        role_manager = portal.acl_users.portal_role_manager
        pas_roles = role_manager.listRoleIds()

    for role in NEW_ROLES:
        if role not in defined_roles:
            portal._addRole(role)
        if HAS_PAS and role not in pas_roles:
            role_manager.addRole(role)

def applyGenericSetupProfile(portal, out):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-eXtremeManagement:default')
    print >> out, "Applied the generic setup profile for eXtremeManagement"
    setup_tool.runAllImportSteps(purge_old=False)
    setup_tool.setImportContext('profile-CMFPlone:plone')

def uninstall(portal):
    """Custom uninstall method for eXtremeManagement."""
    left_slots = portal.getProperty('left_slots', None)
    remainingSlots = [slot for slot in left_slots if slot not in XM_LEFT_SLOTS]
    portal._updateProperty('left_slots', tuple(remainingSlots)) 

    right_slots = portal.getProperty('right_slots', None)
    remainingSlots = [slot for slot in right_slots if slot not in XM_RIGHT_SLOTS]
    portal._updateProperty('right_slots', tuple(remainingSlots)) 

def install(self):
    out = StringIO()

    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)

    addOurRoles(self)
    out.write("Added our extra roles.")
   
    print >> out, "Customize the portal"
    setupSkin(self)
 
    print >> out, "Customizing portal properties"
    configurePortalProps(self)
 
    # Turned off for now.
    #print >> out, "Adding default folders"
    #addFolders(self)
    disableJoinLink(self)

    print >> out, "Integrate our types in kupu, if it is installed."
    configureKupu(self)

    print >> out, "Migrating content"
    migrate_ct(self, out)
    
    print >> out, "Apply the generic setup profile"
    applyGenericSetupProfile(self, out)


    return out.getvalue()

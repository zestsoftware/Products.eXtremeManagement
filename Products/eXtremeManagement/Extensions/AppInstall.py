from StringIO import StringIO
from sets import Set
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ManagePortal
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFDefault.PropertiesTool import PropertiesTool
from Products.Archetypes.public import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.eXtremeManagement.config import *

def removeSkinSelection(portal, out):
    sk_tool = getToolByName(portal, 'portal_skins')
    if 'eXtremeManagement' in sk_tool.getSkinSelections():
        # If eXtremeManagement is the default selection, reset it to
        # Plone Default.
        if sk_tool.getDefaultSkin() == 'eXtremeManagement':
            sk_tool.default_skin = 'Plone Default'
            print >> out, "Set Plone Default as default skin instead of eXtremeManagement."
        # Remove our own skin selection.
        sk_tool.manage_skinLayers(chosen=['eXtremeManagement'],
                                  del_skin='Delete')
        print >> out, "Removed the eXtremeManagement skin selection."

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

    Part of this is done through GenericSetup, but adding roles to the
    PlonePAS role manager does not work there.
    """
    if HAS_PAS:
        role_manager = portal.acl_users.portal_role_manager
        pas_roles = role_manager.listRoleIds()
        for role in NEW_ROLES:
            if role not in pas_roles:
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

    out.write("Successfully installed %s.\n" % PROJECTNAME)
    addOurRoles(self)
    out.write("Added our extra roles.\n")
    removeSkinSelection(self, out)
    print >> out, "Integrate our types in kupu, if it is installed."
    configureKupu(self)
    print >> out, "Migrating content"
    migrate_ct(self, out)
    if HAS_GENERIC_SETUP:
        print >> out, "Apply the generic setup profile"
        applyGenericSetupProfile(self, out)

    return out.getvalue()

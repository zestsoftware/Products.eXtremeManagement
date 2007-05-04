from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.config import *


def reindexIndexes(site):
    """Reindex some indexes.

    Indexes that are added in the catalog.xml file get cleared
    everytime the GenericSetup profile is applied.  So we need to
    reindex them.

    Since we are forced to do that, we might as well make sure that
    these get reindexed in the correct order.  At least id *might*
    help for some of the indexes for estimates and booked hours to be
    reindexed in a specific order.
    """
    cat = getToolByName(site, 'portal_catalog')
    indexes = [
        'getAddress',
        'getAssignees',
        'getBookingDate',
        'getCity',
        'getCountry',
        'getEmail',
        'getFax',
        'getFullname',
        'getHours', # before getRawActualHours, getRawEstimate and
                    # getRawDifference
        'getMinutes', # before getRawActualHours, getRawEstimate and
                      # getRawDifference
        'getName',
        'getPhone',
        'getRawActualHours',
        'getRawEstimate',
        'getEstimate', # after getRawEstimate
        'getRawDifference', # after getRawActualHours and getRawEstimate
        'getRawRelatedItems',
        'getWebsite',
        'getZipCode',
        ]
    # Don't reindex an index if it isn't actually in the catalog.
    # Should not happen, but cannot do any harm.
    ids = [id for id in indexes if id in cat.indexes()]
    if ids:
        cat.manage_reindexIndex(ids=ids)
        

def _migrateSchema(site, contentType):
    at = getToolByName(site, 'archetype_tool')
    class dummy:
        form = {}
    dummyRequest = dummy()
    dummy.form[contentType] = 1
    at.manage_updateSchema(update_all=1,
                           REQUEST=dummyRequest)

def _migrateProjectSchema(site):
    _migrateSchema(site, 'eXtremeManagement.Iteration')

def _migrateIterationSchema(site):
    _migrateSchema(site, 'eXtremeManagement.Iteration')

def _migrateStorySchema(site):
    _migrateSchema(site, 'eXtremeManagement.Story')

def _migrateTaskSchema(site):
    """
    Add a property to the portal so that other parts now that there is
    a schema update going on for the Tasks.  Main reason: if this is
    True, then _do not_ send an email for every Task that is getting
    assigned.  See Task.setAssigned()
    """
    portal_properties = getToolByName(site, 'portal_properties')
    xm_props = portal_properties.xm_properties
    ori = xm_props.send_task_mails
    xm_props.send_task_mails = False
    _migrateSchema(site, 'eXtremeManagement.Task')
    xm_props.send_task_mails = ori


def _migrateBookingSchema(site):
    _migrateSchema(site, 'eXtremeManagement.Booking')

def migrate_stories(portal):
    _migrateStorySchema(portal)

def migrate_tasks(portal):
    _migrateTaskSchema(portal)


def migrate_bookings(portal):
    _migrateBookingSchema(portal)

def migrate_ct(portal):
    migrate_stories(portal)
    migrate_tasks(portal)


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


def removeSkinSelection(portal):
    """Undo mistake from past.
    """
    sk_tool = getToolByName(portal, 'portal_skins')
    if 'eXtremeManagement' in sk_tool.getSkinSelections():
        # If eXtremeManagement is the default selection, reset it to
        # Plone Default.
        if sk_tool.getDefaultSkin() == 'eXtremeManagement':
            sk_tool.default_skin = 'Plone Default'
        # Remove our own skin selection.
        sk_tool.manage_skinLayers(chosen=['eXtremeManagement'],
                                  del_skin='Delete')


def importVarious(context):
    site = context.getSite()
    removeSkinSelection(site)
    addOurRoles(site)
    # Integrate our types in kupu, if it is installed.
    configureKupu(site)
    migrate_ct(site)
    reindexIndexes(site)

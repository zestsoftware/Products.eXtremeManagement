import os.path
from zope.event import notify
try:
    from zope.lifecycleevent import ObjectModifiedEvent
except ImportError:
    # BBB for Zope 2.9
    from zope.app.event.objectevent import ObjectModifiedEvent
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.config import *
from Products.eXtremeManagement.timing.interfaces import IActualHours
from Products.eXtremeManagement.timing.interfaces import IEstimate


def reindexIndexes(site, logger):
    """Reindex some indexes.

    Indexes that are added in the catalog.xml file get cleared
    everytime the GenericSetup profile is applied.  So we need to
    reindex them.

    Since we are forced to do that, we might as well make sure that
    these get reindexed in the correct order.  At least it *might*
    help for some of the indexes for estimates and booked hours to be
    reindexed in a specific order.
    """
    cat = getToolByName(site, 'portal_catalog')
    indexes = [
        'getAssignees',
        'getBookingDate',
        ]
    # Don't reindex an index if it isn't actually in the catalog.
    # Should not happen, but cannot do any harm.
    ids = [id for id in indexes if id in cat.indexes()]
    if ids:
        cat.manage_reindexIndex(ids=ids)
    logger.info('Reindexed getAssignees and getBookingDate')


def _migrateSchema(site, contentType, logger):
    at = getToolByName(site, 'archetype_tool')
    class dummy:
        form = {}
    dummyRequest = dummy()
    dummy.form[contentType] = 1
    at.manage_updateSchema(update_all=1,
                           REQUEST=dummyRequest)
    logger.info('Migrated schema of %s', contentType)

def _migrate_project(portal, logger):
    _migrateSchema(portal, 'eXtremeManagement.Project', logger)

def _migrate_iterations(portal, logger):
    _migrateSchema(portal, 'eXtremeManagement.Iteration', logger)

def migrate_stories(portal, logger):
    _migrateSchema(portal, 'eXtremeManagement.Story', logger)

def migrate_tasks(portal, logger):
    """
    Add a property to the portal so that other parts now that there is
    a schema update going on for the Tasks.  Main reason: if this is
    True, then _do not_ send an email for every Task that is getting
    assigned.  See Task.setAssigned()
    """
    portal_properties = getToolByName(portal, 'portal_properties')
    xm_props = portal_properties.xm_properties
    ori = xm_props.send_task_mails
    xm_props.send_task_mails = False
    _migrateSchema(portal, 'eXtremeManagement.Task', logger)
    _migrateSchema(portal, 'eXtremeManagement.PoiTask', logger)
    xm_props.send_task_mails = ori

def migrate_bookings(portal, logger):
    _migrateSchema(portal, 'eXtremeManagement.Booking', logger)

def migrate_ct(portal, logger):
    #migrate_projects(portal, logger)
    #migrate_iterations(portal, logger)
    migrate_stories(portal, logger)
    migrate_tasks(portal, logger)
    migrate_bookings(portal, logger)


def configureKupu(portal, logger):
    """In Plone 3.0 / kupu 1.4 we can actually use a kupu.xml file
    instead, which is better.
    """
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
    logger.info('Added our types to collection and linkable of kupu')


def removeSkinSelection(portal, logger):
    """Undo mistake from past.
    """
    sk_tool = getToolByName(portal, 'portal_skins')
    if 'eXtremeManagement' in sk_tool.getSkinSelections():
        # If eXtremeManagement is the default selection, reset it to
        # Plone Default.
        if sk_tool.getDefaultSkin() == 'eXtremeManagement':
            sk_tool.default_skin = 'Plone Default'
            logger.info('Default skin reset from eXtremeManagement to Plone Default.')
        # Remove our own skin selection.
        sk_tool.manage_skinLayers(chosen=['eXtremeManagement'],
                                  del_skin='Delete')
        logger.info('Removed eXtremeManagement skin selection.')


def annotate_actual(site, logger):
    """Make sure the right types are annotated with IActualHours.
    This updates the catalog too, which is nice.
    """
    cat = getToolByName(site, 'portal_catalog')
    for portal_type in ('Booking', 'Task', 'PoiTask', 'Story', 'Iteration'):
        brains = cat(portal_type=portal_type)
        for brain in brains:
            obj = brain.getObject()
            anno = IActualHours(obj)
            anno.recalc()
    logger.info('Annotated types with IActualHours')


def annotate_estimate(site, logger):
    """Make sure the right types are annotated with IEstimate.
    This updates the catalog too, which is nice.
    """
    cat = getToolByName(site, 'portal_catalog')
    for portal_type in ('Task', 'PoiTask', 'Story', 'Iteration'):
        brains = cat(portal_type=portal_type)
        for brain in brains:
            obj = brain.getObject()
            anno = IEstimate(obj)
            anno.recalc()
    logger.info('Annotated types with IEstimate')


def update_security_settings(site, logger):
    workflow = getToolByName(site, 'portal_workflow')
    workflow.updateRoleMappings()
    logger.info('Updated security (workflow) settings')


def importVarious(context):
    # Only run step if a flag file is present
    if context.readDataFile('extrememanagement_various.txt') is None:
        return
    logger = context.getLogger('eXtremeManagement')
    site = context.getSite()
    removeSkinSelection(site, logger)
    # Integrate our types in kupu, if it is installed.
    configureKupu(site, logger)
    migrate_ct(site, logger)
    update_security_settings(site, logger)
    annotate_actual(site, logger)
    annotate_estimate(site, logger)
    reindexIndexes(site, logger)
    logger.info('eXtremeManagement_various step imported')


def from_plone25_to_30(context):
    # Right, context == portal_setup here.
    context.runAllImportStepsFromProfile(
        'profile-Products.eXtremeManagement:eXtremeManagement-30-types',
        purge_old=False)

import transaction
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement import config
from Products.eXtremeManagement.timing.interfaces import IActualHours
from Products.eXtremeManagement.timing.interfaces import IEstimate


def install_dependencies(site, logger):
    qi = getToolByName(site, 'portal_quickinstaller')
    for product in config.DEPENDENCIES:
        if not qi.isProductInstalled(product):
            qi.installProduct(product)
            transaction.savepoint(optimistic=True)
            logger.info("Installed %s.", product)
    # Now reinstall all products for good measure.
    qi.reinstallProducts(config.DEPENDENCIES)
    logger.info("Reinstalled %s.", config.DEPENDENCIES)

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
    #migrate_stories(portal, logger)
    #migrate_tasks(portal, logger)
    #migrate_bookings(portal, logger)
    # Nothing needed at the moment.
    pass


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

    for type in config.OUR_LINKABLE_TYPES:
        if type not in linkable:
            linkable.append(type)

    for type in config.OUR_COLLECTION_TYPES:
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


def add_roles_that_should_be_handled_by_rolemap_xml(site, logger):
    role_manager = site.acl_users.portal_role_manager
    pas_roles = role_manager.listRoleIds()
    for role in config.NEW_ROLES:
        if role not in pas_roles:
            role_manager.addRole(role)
            logger.info('Added role %s', role)


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


def importVarious(context):
    # Only run step if a flag file is present
    if context.readDataFile('extrememanagement_various.txt') is None:
        return
    logger = context.getLogger('eXtremeManagement')
    site = context.getSite()
    install_dependencies(site, logger)
    # Integrate our types in kupu, if it is installed.
    configureKupu(site, logger)
    migrate_ct(site, logger)
    #annotate_actual(site, logger)
    #annotate_estimate(site, logger)
    add_roles_that_should_be_handled_by_rolemap_xml(site, logger)
    reindexIndexes(site, logger)
    logger.info('eXtremeManagement_various step imported')


def from_plone25_to_30(context):
    # Right, context == portal_setup here.
    context.runAllImportStepsFromProfile(
        'profile-Products.eXtremeManagement:eXtremeManagement-30-types',
        purge_old=False)

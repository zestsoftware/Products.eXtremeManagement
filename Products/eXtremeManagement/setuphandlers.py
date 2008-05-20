from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement import config


def addCatalogIndexes(site, logger):
    """Add our indexes to the catalog.

    Doing it here instead of in profiles/default/catalog.xml means we
    do not need to reindex those indexes after every reinstall.
    """
    catalog = getToolByName(site, 'portal_catalog')
    indexes = catalog.indexes()
    wanted = (("getAssignees", "KeywordIndex"),
              ("getBookingDate", "DateIndex"))

    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            logger.info("Added %s for field %s.", meta_type, name)


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
    kupuTool.updateResourceTypes(({'resource_type': 'linkable',
                                   'old_type': 'linkable',
                                   'portal_types': linkable},
                                  {'resource_type': 'collection',
                                   'old_type': 'collection',
                                   'portal_types': collection},
                                  ))
    logger.info('Added our types to collection and linkable of kupu')


def add_roles_that_should_be_handled_by_rolemap_xml(site, logger):
    role_manager = site.acl_users.portal_role_manager
    pas_roles = role_manager.listRoleIds()
    for role in config.NEW_ROLES:
        if role not in pas_roles:
            role_manager.addRole(role)
            logger.info('Added role %s', role)


def importVarious(context):
    # Only run step if a flag file is present
    if context.readDataFile('extrememanagement_various.txt') is None:
        return
    logger = context.getLogger('eXtremeManagement')
    site = context.getSite()
    # Integrate our types in kupu, if it is installed.
    configureKupu(site, logger)
    add_roles_that_should_be_handled_by_rolemap_xml(site, logger)
    addCatalogIndexes(site, logger)
    logger.info('eXtremeManagement_various step imported')

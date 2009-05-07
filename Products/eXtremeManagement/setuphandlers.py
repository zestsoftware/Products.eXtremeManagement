from Products.ATContentTypes.lib.constraintypes import ENABLED
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.interfaces import ISelectableConstrainTypes
from Products.contentmigration.archetypes import ATFolderMigrator
from Products.contentmigration.basemigrator.walker import CatalogWalker
from plone.app.portlets import portlets as plone_portlets
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager
from zope.component import getUtility, getMultiAdapter

from Products.eXtremeManagement import config


def addCatalogIndexes(site, logger):
    """Add our indexes to the catalog.

    Doing it here instead of in profiles/default/catalog.xml means we
    do not need to reindex those indexes after every reinstall.
    """
    catalog = getToolByName(site, 'portal_catalog')
    indexes = catalog.indexes()
    wanted = (("getAssignees", "KeywordIndex"),
              ("getBookingDate", "DateIndex"),
              ("getBillableProject", "FieldIndex"),
              ("getEndDate", "DateIndex"),
             )
    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
            logger.info("Added %s for field %s.", meta_type, name)
    if len(indexables) > 0:
        logger.info("Indexing new indexes %s.", ', '.join(indexables))
        catalog.manage_reindexIndex(ids=indexables)


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


def upgrade_from_16_to_20(context):
    site = getToolByName(context, 'portal_url').getPortalObject()
    types = dict(ProjectFolder='Folder', CustomerFolder='Folder')

    class ProjectFolderMigrator(ATFolderMigrator):
        src_portal_type = src_meta_type = 'ProjectFolder'
        dst_portal_type = dst_meta_type = 'Folder'
        new_allowed = ('Project', )

        def migrate_typerestriction(self):
            constraints = ISelectableConstrainTypes(self.new)
            constraints.setConstrainTypesMode(ENABLED)
            constraints.setImmediatelyAddableTypes(self.new_allowed)
            constraints.setLocallyAllowedTypes(self.new_allowed)

    projectfolders = CatalogWalker(site, ProjectFolderMigrator)
    projectfolders.go()

    class CustomerFolderMigrator(ProjectFolderMigrator):
        src_portal_type = src_meta_type = 'CustomerFolder'
        dst_portal_type = dst_meta_type = 'Folder'
        new_allowed = ('Customer', )

    customerfolders = CatalogWalker(site, CustomerFolderMigrator)
    customerfolders.go()


def zap_old_xm_portlets(site, logger):
    """Zap several known old-style xm portlets."""
    to_zap = ('portlet_poi',
              'portlet_stories',
              'portlet_my_projects',
              )
    column = getUtility(IPortletManager, name="plone.leftcolumn", context=site)
    manager = getMultiAdapter((site, column), IPortletAssignmentMapping)
    old_style = [key for key in manager.keys() if
                 isinstance(manager[key], plone_portlets.classic.Assignment)]
    to_delete = [key for key in old_style
                 if manager[key].template in to_zap]
    for key in to_delete:
        del manager[key]
        logger.info("Removed old-style %s portlet", key)


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
    zap_old_xm_portlets(site, logger)
    logger.info('eXtremeManagement_various step imported')

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
    newSlots = ('here/portlet_stories/macros/portlet',)
    for slot in newSlots:
        if slot not in left_slots:
            portal._updateProperty('left_slots', tuple(left_slots) + (slot,)) 

    right_slots = portal.getProperty('right_slots', None)
    newSlots = ('here/portlet_tasks/macros/portlet',)
    for slot in newSlots:
        if slot not in right_slots:
            portal._updateProperty('right_slots', tuple(right_slots) + (slot,)) 

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
    _migrateSchema(self, 'eXtremeManagement.Task')

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
    kupuTool = getToolByName(portal, 'kupu_library_tool')
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


def enablePortalFactory(portal):
    # enable portal_factory for given types
    factory_tool = getToolByName(portal,'portal_factory')
    factory_types=[
        ] + factory_tool.getFactoryTypes().keys()
    for type in OUR_FACTORY_TYPES:
        if type not in factory_types:
            factory_types.append(type)
    factory_tool.manage_setPortalFactoryTypes(listOfTypeIds=factory_types)


def install(self):
    out = StringIO()
    installTypes(self, out,
                 listTypes(PROJECTNAME),
                 PROJECTNAME)

    install_subskin(self, out, GLOBALS)

    out.write("Successfully installed %s." % PROJECTNAME)
   
    print >> out, "Customize the portal"
    setupSkin(self)
 
    print >> out, "Customizing portal properties"
    configurePortalProps(self)
 
    # Turned off for now.
    #print >> out, "Adding default folders"
    #addFolders(self)
    disableJoinLink(self)

    print >> out, "Integrate our types in kupu"
    configureKupu(self)

    print >> out, "Migrating content"
    migrate_ct(self, out)

    print >> out, "Enabling portal_factory for our types"
    enablePortalFactory(self)

    return out.getvalue()

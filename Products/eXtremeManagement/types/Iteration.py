from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

from Products.Archetypes.BaseFolder import BaseFolder
from Products.Archetypes.interfaces.orderedfolder import IOrderedFolder
from Products.Archetypes import OrderedBaseFolder
from Products.Archetypes.OrderedBaseFolder import OrderedBaseFolder

schema = BaseFolderSchema + DescriptionSchema + IterationSchema

class Iteration(OrderedBaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'iteration_icon.gif'
    meta_type             = 'Iteration'
    archetype_name        = 'Iteration'
    product_meta_type     = 'Iteration'
    immediate_view        = 'iteration_view'
    default_view          = 'iteration_view'
    allowed_content_types = (['Story',])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()


    def _get_stories(self):
        """ returns a list of the unassigned stories """
        catalog_tool = getToolByName(self, 'portal_catalog')
        stories = catalog_tool.searchResults(portal_type='Story')
        list = []
        for story in stories:
            list.append(story.Title)

        return list


    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/iteration_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Iteration, PROJECTNAME)



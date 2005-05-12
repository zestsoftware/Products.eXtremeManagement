from Products.Archetypes.public import *
from Products.CMFCore import CMFCorePermissions
from AccessControl import ClassSecurityInfo
from Products.eXtremeManagement.schemata import *
from Products.eXtremeManagement.config import *

schema = BaseFolderSchema + DescriptionSchema + StorySchema

class Story(BaseFolder):
    """A simple folderish archetype"""
    schema                = schema
    content_icon          = 'story_icon.gif'
    meta_type             = 'Story'
    archetype_name        = 'Story'
    product_meta_type     = 'Story'
    immediate_view        = 'story_view'
    default_view          = 'story_view'
    allowed_content_types = (['Task', 'Document',])
    global_allow          = 0
    typeDescription       = ''
    typeDescMsgId         = ''
    security              = ClassSecurityInfo()


    def CookedBody(self):
        """Dummy attribute to allow drop-in replacement of Document"""
        return self.getMainText()


    actions = (
               {
                'id': 'view',
                'name': 'View',
                'action': 'string:${object_url}/story_view',
                'permissions': (CMFCorePermissions.View,),
                'category': 'object'
               },
              )

registerType(Story, PROJECTNAME)



from Products.CMFCore.CMFCorePermissions import AddPortalContent, ManagePortal
from Products.Archetypes.public import DisplayList

ADD_CONTENT_PERMISSION = AddPortalContent
PROJECTNAME = 'eXtremeManagement'
SKINS_DIR = 'skins'

GLOBALS = globals()

configlets = (
              {'id': 'XPProjectManagement',
               'appId': 'eXtremeMangement',
               'name': 'eXtreme Project Mangement',
               'action': 'string:$portal_url/prefs_project_management',
               'category': 'Products',
               'permission': ManagePortal,
               'imageUrl': 'folder_icon.gif'
              },
             )


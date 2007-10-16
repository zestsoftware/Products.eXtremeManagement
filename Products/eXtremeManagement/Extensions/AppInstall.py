from StringIO import StringIO
from sets import Set
from Products.CMFCore.utils import getToolByName
from Products.eXtremeManagement.config import *


def applyGenericSetupProfile(portal, out):
    setup_tool = getToolByName(portal, 'portal_setup')
    setup_tool.setImportContext('profile-eXtremeManagement:default')
    print >> out, "Applying the generic setup profile for eXtremeManagement..."
    setup_tool.runAllImportSteps(purge_old=False)
    setup_tool.setImportContext('profile-Products.CMFPlone:plone')
    print >> out, "Applied the generic setup profile for eXtremeManagement"


def removeOldTool(portal, out):
    if 'xm_tool' in portal.objectIds():
        portal.manage_delObjects('xm_tool')
        print >> out, "Removed outdated xm_tool from portal."


def uninstall(portal):
    """Custom uninstall method for eXtremeManagement."""
    out = StringIO()
    removeOldTool(portal, out)

    left_slots = portal.getProperty('left_slots', None)
    remainingSlots = [slot for slot in left_slots if slot not in XM_LEFT_SLOTS]
    portal._updateProperty('left_slots', tuple(remainingSlots)) 

    right_slots = portal.getProperty('right_slots', None)
    remainingSlots = [slot for slot in right_slots if slot not in XM_RIGHT_SLOTS]
    portal._updateProperty('right_slots', tuple(remainingSlots)) 
    return out.getvalue()


def install(self):
    out = StringIO()
    removeOldTool(self, out)
    print >> out, "Apply the generic setup profile"
    applyGenericSetupProfile(self, out)
    out.write("Successfully installed %s.\n" % PROJECTNAME)

    return out.getvalue()

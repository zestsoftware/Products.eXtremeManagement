from Products.CMFPlone.Portal import addPolicy
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.Expression import Expression
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.DirectoryView import addDirectoryViews, registerDirectory
from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy

class eXtremeManagementPolicy(DefaultCustomizationPolicy):
    """ Customize plone for eXtremeManagement """

    def customize(self, portal):
        # Install the Plone Site with the default policy and
        # update it with this one. All changes to standard
        # Plone will be done in this policy.



        # add new roles
        newRoles = ['Employee', 'Customer']
        defined_roles = getattr(portal, '__acl_roles__', ())

        for role in newRoles:
            if not role in defined_roles:
                portal._addRole(role)


def register(context, app_state):
    addPolicy('eXtremeManagement', eXtremeManagementPolicy())

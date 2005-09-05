from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy
from Products.CMFPlone.Portal import addPolicy
from Products.CMFCore.utils import getToolByName
from config import PROJECTNAME
from zLOG import LOG, INFO
from Products.CMFCore.Expression import Expression
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.DirectoryView import addDirectoryViews, registerDirectory
from Products.CMFPlone.CustomizationPolicy import DefaultCustomizationPolicy


class eXtremeManagementPolicy(DefaultCustomizationPolicy):
    """ Customize plone for eXtremeManagement """


    def customize(self, portal):
        """ custom customize method
        """
        # If the customization Policy id called inside an already existing
        # portal, calling the DefaultCustomizationPolicy.customize is a
        # problem
        # ugly try catch arround works, but should somewhere in future be
        # replaced by a test from which location we are calling.
        try:
            DefaultCustomizationPolicy.customize(self, portal)
        except:
            pass

        # call all methods starting with 'customize'
        LOG(PROJECTNAME, INFO, "Customization Policy applied:")
        for method in dir(self):
            if method.startswith('customize') and method!='customize':
                print "Processing customization '%s' ..." % method
                eval('self.%s(portal)' % method)

    def customize_1_InstallProducts(self, portal):
        """ Install the product

        Note that you can add dependencies to the DEPENDENCIES list in
        config.py, these are auto-installed by Install.py so no need
        to add them here.
        """
        portal.portal_quickinstaller.installProduct(PROJECTNAME)
        get_transaction().commit(1)

    # define your own customize_#_name methods after this line:

        # add new roles
        newRoles = ['Employee', 'Customer']
        defined_roles = getattr(portal, '__acl_roles__', ())

        for role in newRoles:
            if not role in defined_roles:
                portal._addRole(role)



def register(context):
    addPolicy('xxx_name_this', xxx_name_thisCustomizationPolicy())



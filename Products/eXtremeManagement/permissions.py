"""
$Id: $
"""
from AccessControl import Permissions as ZPerms
from Products.CMFCore import CMFCorePermissions as CMFPerms
from Products.GroupUserFolder import GroupsToolPermissions as GRUFPerms
from Products.CMFCore.CMFCorePermissions import setDefaultRoles
from utils import ContentPermMap


# Roles
eXtremeManagementRoles = ['Employee', 'Customer',]

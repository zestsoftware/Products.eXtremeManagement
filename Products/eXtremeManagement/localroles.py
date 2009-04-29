from zope.interface import implements
from plone.app.workflow.interfaces import ISharingPageRole

# Please keep this 'PMF' and not '_' as otherwise i18ndude picks it
# up, does not realize it is for the plone domain and puts it in the
# pot/po files of xm.  Alternatively: exclude this file in
# rebuild_i18n.sh
from Products.CMFPlone import PloneMessageFactory as PMF


class EmployeeRole(object):
    implements(ISharingPageRole)

    title = PMF(u"title_employee_role",
                default="Works on project")
    required_permission = 'eXtremeManagement: Add Project'


class CustomerRole(object):
    implements(ISharingPageRole)

    title = PMF(u"title_customer_role",
                default="Customer can track project")
    required_permission = 'eXtremeManagement: Add Project'


class ProjectmanagerRole(object):
    implements(ISharingPageRole)

    title = PMF(u"title_projectmanager_role",
                default="Can manage project")
    required_permission = 'Manage portal'

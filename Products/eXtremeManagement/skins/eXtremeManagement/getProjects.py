## Script (Python) "getProjects"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Return the Projects in the ProjectFolder 
##


# Where do we want to search?
object = context
searchpath = '/'.join(object.getPhysicalPath())

projects = context.portal_catalog.searchResults(portal_type='Project',
                                                path=searchpath)
list = []

for project in projects:
    project = project.getObject()
    list.append(project)

return list

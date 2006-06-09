## Script (Python) "formatTime"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=time=0
##title=Return the formatted time.
##

"""
This script ensures that you can call formatTime even when you are not
somewhere in a ProjectFolder.

This should disappear after the merge with the lovely branch as they
solve it better.
"""

# HACK: find a ProjectFolder so we can call the formatTime() function
# from that projectfolder later.
pf = context.portal_catalog.searchResults(portal_type='ProjectFolder')
projectFolder = pf[0].getObject()
formatTime = projectFolder.formatTime
return formatTime(time)

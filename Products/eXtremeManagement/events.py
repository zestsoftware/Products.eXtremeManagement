from Products.CMFCore.utils import getToolByName

def addedBooking(object, event):
    """A Booking was added, moved or removed.
    So we reindex the old and new containers, if they exist.
    """
    cat = getToolByName(object, 'portal_catalog')
    if event.oldParent is not None:
        cat.reindexObject(event.oldParent)
    if event.newParent is not None:
        cat.reindexObject(event.newParent)


def modifiedBooking(object, event):
    """A Booking was modified.
    So we reindex its parent too.
    """
    # making eXtremeManagement portal_factory-aware is a bit gross but
    # as long as a Booking's state influences it's parent Task, we need
    # to make speed optimizations like this - Rocky
    factory = getToolByName(object, 'portal_factory')
    if not factory.isTemporary(object):
         parent = object.aq_inner.aq_parent
         parent.reindexObject()

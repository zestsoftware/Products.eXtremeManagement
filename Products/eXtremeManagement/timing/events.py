from Acquisition import aq_inner, aq_parent

from interfaces import IActualHours
from interfaces import IEstimate


def recursivelyRecalc(object, adapter):
    current = aq_inner(object)
    anno = adapter(current, None)
    while anno is not None:
        anno.recalc()
        current = aq_parent(current)
        anno = adapter(current, None)


def addedActualHours(object, event):
    """An object with actual hours (a Booking or a parent usually) was
    added, moved or removed.  So we reindex the old and new
    containers, if they exist.

    Some notes.

    Adding Bookings
    ---------------

    When *adding* a Booking in the browser the IObjectMovedEvent is
    fired more often than you would care to know.  But it is important
    to understand this anyway, so we had better care.

    All events are IObjectAddedEvents, except for the last one, which
    is an IObjectMovedEvent.  Note though that IObjectAddedEvents
    inherits from IObjectMovedEvent.

    1. The Booking is first created in the portal factory.

      - event.oldParent is None.

      - event.newParent is then a TempFolder

    2. This event is called a second time with those settings.  After
       this, you can fill in values in your browser.

    3. Then in the browser you click save so the event is fired again.

      - event.oldParent is None.

      - event.NewParent is still a TempFolder

    4. Then the event is fired another time:

      - event.oldParent is None.

      - event.newParent is a Task (unless you allow Bookings to be
        added in other content types)

      - nothing has been filled in yet, specifically the Booking has
        no hours or minutes yet

    5. Then the final step:

      - event.oldParent is a Task.

      - event.newParent is that same Task (!).  Ah, Martijn Pieters is
        right in saying that this is because the Booking is renamed.
        Makes sense.

      - So this is an IObjectMovedEvent.

      - the Booking now has values.

    This last time is the only time that we actually want to do
    something in this event handler.

    Actually, it looks like even that last time we do not have to do
    anything.  The Booking with hours and minutes is already in the
    Task and is just renamed.  At this point the total in the Task has
    already been recalculated, courtesy of the event handler that
    listens to IObjectModifiedEvents.


    When moving a Booking:
    ----------------------

    - oldParent is the old parent Task

    - newParent is the new parent Task

    
    When removing a Booking:
    ------------------------

    - oldParent is the old parent Task

    - newParent is None
    

    Moving a parent
    ---------------

    One more gotcha: when moving a Task with a child Booking to a new
    location, the parent of the Booking will remain that same Task, so
    no event really has to be handled here.  But the event of the Task
    moving to a new parent is actually dispatched to all its childs.
    In that case the object is a Booking and event.newParent is a
    Story, which seems strange.  In that case you need to be aware
    that event.object is that Task.

    So using an event a Booking is told that his parent has moved to a
    newParent.  In this event handler we do not have to do anything
    then.

    See zope.app.container.contained.py:dispatchToSublocations() which
    says: This suggests that location event handlers need to be aware
    that the objects they are called on and the event objects could be
    different.

    """
    if object != event.object:
        # The parent itself has moved and we do not care.
        return
    if event.oldParent == event.newParent:
        # Just a rename, so never mind
        return
    anno = IActualHours(object)
    if anno.actual_time == 0.0:
        # Nothing needs to be done here.
        return
    for parent in (event.oldParent, event.newParent):
        recursivelyRecalc(parent, IActualHours)


def modifiedActualHours(object, event):
    """An object with actual hours (a Booking or a parent usually) was
    modified.  So we reindex its parent too.
    """
    recursivelyRecalc(object, IActualHours)


def addedEstimate(object, event):
    """An object with an estimate (a Task or its parent usually) was
    added, moved or removed.  So we reindex the old and new
    containers, if they exist.
    """
    if object != event.object:
        # The parent itself has moved and we do not care.
        return
    if event.oldParent == event.newParent:
        # Just a rename, so never mind
        return
    anno = IEstimate(object)
    if anno.estimate == 0.0:
        # Nothing needs to be done here.
        return
    for parent in (event.oldParent, event.newParent):
        recursivelyRecalc(parent, IEstimate)


def modifiedEstimate(object, event):
    """An object with estimates (a Task or its parent usually) was
    modified.  So we reindex its parent too.
    """
    recursivelyRecalc(object, IEstimate)

def formatTime(time):
    """Returns time as a formatted string

    >>> formatTime(0)
    '0:00'
    >>> formatTime(-0.6)
    '-0:36'
    >>> formatTime(0.6)
    '0:36'
    >>> formatTime(-1)
    '-1:00'
    >>> formatTime(1)
    '1:00'
    >>> formatTime(1.5)
    '1:30'
    >>> formatTime(-1.5)
    '-1:30'

    Now try some times that might give problems, e.g.:
    .04*60 equals 2.3999999999999999, which should be rounded down

    >>> formatTime(0.04)
    '0:02'
    >>> formatTime(8.05)
    '8:03'
    >>> formatTime(44.5)
    '44:30'
    >>> formatTime(0.999)
    '1:00'

    """
    try:
        hours = int(time)
        minutes = int(round((time - hours)*60))
    except TypeError:
        return '?:??'
    # Adjust for rounding:
    if minutes == 60:
        minutes = 0
        hours += 1
    if hours == 0 and minutes == 0:
        return ('0:00')
    minutes = abs(minutes)
    hours = abs(hours)
    minutes = _formatMinutes(minutes)
    # This should not happen:
    if minutes is False:
        minutes = ':ERROR'
    sign = ''
    if time < 0:
        sign = '-'
    return ('%s%s%s' % (sign, hours, minutes))


def _formatMinutes(minutes):
    """Takes the integer argument minutes and formats it nicely.

    >>> _formatMinutes(0)
    ':00'
    >>> _formatMinutes(5)
    ':05'
    >>> _formatMinutes(42)
    ':42'
    >>> _formatMinutes(59)
    ':59'

    minutes should be between 0 and 59

    >>> _formatMinutes(-1)
    False
    >>> _formatMinutes(60)
    False

    """
    minutes = int(minutes)
    if minutes < 0:
        return False
    if minutes > 59:
        return False
    if minutes < 10:
        minutes = '0%s' % minutes
    minutes = ':%s' % minutes
    return minutes


def getStateSortedContents(items):
    """Get completed/invoiced items first, then rest of ordered folder contents

    We start simple: an empty list should simply return an empty list:

    >>> getStateSortedContents([])
    []

    items should have an attribute review_state:

    >>> getStateSortedContents([1,2])
    Traceback (most recent call last):
    ...
    AttributeError: 'int' object has no attribute 'review_state'

    We make a simple test class for items.

    >>> class Item(object):
    ...     def __init__(self, state):
    ...         self.review_state = state
    ...     def __repr__(self):
    ...         # Nicer for testing
    ...         return self.review_state

    We make some test items:

    >>> private = Item('private')
    >>> public = Item('public')
    >>> completed = Item('completed')
    >>> invoiced = Item('invoiced')

    Some simple tests with only items in one category:

    >>> getStateSortedContents([private, public])
    [private, public]
    >>> getStateSortedContents([public, private])
    [public, private]
    >>> getStateSortedContents([completed, invoiced])
    [completed, invoiced]

    Now for the real tests.

    >>> getStateSortedContents([private, public, completed, invoiced])
    [completed, invoiced, private, public]
    >>> getStateSortedContents([public, invoiced, private, completed])
    [invoiced, completed, public, private]

    """
    firstStates = ['completed', 'invoiced']
    firstItems = []
    otherItems = []
    for item in items:
        if item.review_state in firstStates:
            firstItems.append(item)
        else:
            otherItems.append(item)
    return firstItems + otherItems


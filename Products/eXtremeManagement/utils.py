from DateTime import DateTime


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

    What if we try to crash the function?

    >>> formatTime('foo')
    '?:??'

    """
    try:
        hours = int(time)
        minutes = int(round((time - hours)*60))
    except ValueError:
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


def getNextYearMonth(year, month):
    """Get the year and month for next month (watch out for December)

    >>> getNextYearMonth(2007, 1)
    (2007, 2)
    >>> getNextYearMonth(2006, 12)
    (2007, 1)

    What happens when we use a wrong month number?

    >>> getNextYearMonth(2007, 13)
    Traceback (most recent call last):
    ...
    ValueError
    >>> getNextYearMonth(2007, 0)
    Traceback (most recent call last):
    ...
    ValueError

    """
    if month < 1 or month > 12:
        raise ValueError
    nextyear = year + month/12
    nextmonth = (month % 12) + 1
    return (nextyear, nextmonth)


def getPrevYearMonth(year, month):
    """Get the year and month for the previous month (watch out for January)

    >>> getPrevYearMonth(2007, 2)
    (2007, 1)
    >>> getPrevYearMonth(2007, 1)
    (2006, 12)

    What happens when we use a wrong month number?

    >>> getPrevYearMonth(2007, 13)
    Traceback (most recent call last):
    ...
    ValueError
    >>> getPrevYearMonth(2007, 0)
    Traceback (most recent call last):
    ...
    ValueError

    Now test this in combination with getNextYearMonth.  These two
    functions should be the reverse of each other.  So this should
    return nothing.  (Note: month range 1 to 13 excludes 13.)

    >>> for month in range(1,13):
    ...     y, m = getNextYearMonth(2007, month)
    ...     if not getPrevYearMonth(y, m) == (2007, month):
    ...         print month
    ...     y, m = getPrevYearMonth(2007, month)
    ...     if not getNextYearMonth(y, m) == (2007, month):
    ...         print month


    """
    if month < 1 or month > 12:
        raise ValueError
    prevmonth = month - 1
    prevyear = year
    if prevmonth == 0:
        prevyear = year - 1
        prevmonth = 12
    return (prevyear, prevmonth)


def getEndOfMonth(year, month):
    """Get the last second of the last day of this month

    First some normal months.

    >>> getEndOfMonth(2007, 1)
    DateTime('2007/01/31 23:59:59 GMT+1')
    >>> getEndOfMonth(2007, 4)
    DateTime('2007/04/30 23:59:59 GMT+2')

    Of course February needs extra testing.

    >>> getEndOfMonth(2007, 2)
    DateTime('2007/02/28 23:59:59 GMT+1')

    2008 is a leap year.

    >>> getEndOfMonth(2008, 2)
    DateTime('2008/02/29 23:59:59 GMT+1')

    """
    if month in (1, 3, 5, 7, 8, 10, 12):
        day = 31
    elif month == 2:
        if DateTime(year, 1, 1).isLeapYear():
            day = 29
        else:
            day = 28
    else:
        day = 30
    return DateTime.latestTime(DateTime(year, month, day))

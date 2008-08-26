from zope.interface import Interface


class IXMIteration(Interface):
    """eXtremeManagement Iteration

    An Iteration is usually a period of a few weeks.  During that
    Iteration you implement some Stories for the customer.

    So an Iteration can contain Stories.
    """

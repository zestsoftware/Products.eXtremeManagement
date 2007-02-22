from zope.interface import Interface


class IXMStory(Interface):
    """eXtremeManagement Story

    A Story is a feature or a coherent set of features that together
    tell a story that the customer wants implemented.  This Story
    should not be bigger than a few days.

    A Story contains Tasks.  When all Tasks are finished, the Story
    should be finished as well.
    """

from zope.interface import Interface


class IXMProject(Interface):
    """eXtremeManagement Project

    Folder where you add information about a project.  In Extreme
    Programming terms this can also function as a Release.

    A Project can at least contain Iterations.
    """

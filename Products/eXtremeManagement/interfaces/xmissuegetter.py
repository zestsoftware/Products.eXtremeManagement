from zope.interface import Interface


class IXMIssueGetter(Interface):
    """eXtremeManagement IssueGetter

    An issuegetter will get a list of brains ( issues )

    """

    def get_issues():
        """Get a list of issue brains
        """


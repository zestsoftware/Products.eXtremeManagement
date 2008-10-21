"""Provides schema and mixin class(es) that should be shared across all
XM unit content types.  Currently this means: Iteration, Story, and Task.
"""

import AccessControl
from Products.Archetypes import atapi
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget \
     import ReferenceBrowserWidget

unit_shared_schema = atapi.Schema((

    # read-only because only private code should be able to setup
    # what content item this item was carried over from
    atapi.ReferenceField(
        name='carriedOverFrom',
        mode='r',
        relationship='carried_over_from',
        allowed_types=('Iteration', 'Story', 'Task'),
        multiValued=False,
        widget=ReferenceBrowserWidget(
            label='Carried Over From',
            label_msgid='eXtremeManagement_label_carriedOverFrom',
            i18n_domain='eXtremeManagement'
            ),
    ),
))

class UnitSharedMixin(object):
    """
    """

    security  = AccessControl.ClassSecurityInfo()

    def getRawCarriedOverFrom(self):
        field = unit_shared_schema['carriedOverFrom']
        return field.getRaw(self)

    def getCarriedOverFrom(self):
        field = unit_shared_schema['carriedOverFrom']
        return field.get(self)

    security.declarePrivate('setCarriedOverFrom')
    def setCarriedOverFrom(self, value):
        field = unit_shared_schema['carriedOverFrom']
        return field.set(self, value)

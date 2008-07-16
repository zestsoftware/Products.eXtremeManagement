from zope.formlib import form
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from plone.app.controlpanel.form import ControlPanelForm
from plone.fieldsets.fieldsets import FormFieldsets
from plone.app.form.validators import null_validator

from xm.booking.timing.interfaces import IActualHours
from xm.booking.timing.interfaces import IEstimate
from Products.eXtremeManagement import XMMessageFactory as _


class XMControlPanel(ControlPanelForm):
    form_fields = FormFieldsets()
    label = _(u"eXtremeManagement maintenance")
    description = _(
        u"Perform various maintenance tasks. "
        "If you know the totals are wrong, you can recalculate them here. "
        "This should normally not be needed, so do not touch this unless "
        "you know what you are doing.  Then again, it does not hurt, except "
        "that it takes a long time.")

    @form.action(
        _(u'label_recalculate_actual_hours',
          default=u'Recalculate actual hours'),
        name=u'recalculate_actual_hours',
        validator=null_validator)
    def recalculate_actual(self, action, data):
        """Recalculate the actual hours.

        Can be used in case the totals are wrong for some reason.
        """
        context = aq_inner(self.context)
        cat = getToolByName(context, 'portal_catalog')
        for portal_type in ('Booking', 'Task', 'PoiTask',
                            'Story', 'Iteration'):
            brains = cat(portal_type=portal_type)
            for brain in brains:
                obj = brain.getObject()
                anno = IActualHours(obj)
                anno.recalc()

    @form.action(
        _(u'label_recalculate_estimated_time',
          default=u'Recalculate estimated time'),
        name=u'recalculate_estimated_time',
        validator=null_validator)
    def recalculate_estimate(self, action, data):
        """Recalculate the estimates.

        Can be used in case the totals are wrong for some reason.
        """
        context = aq_inner(self.context)
        cat = getToolByName(context, 'portal_catalog')
        for portal_type in ('Task', 'PoiTask', 'Story', 'Iteration'):
            brains = cat(portal_type=portal_type)
            for brain in brains:
                obj = brain.getObject()
                anno = IEstimate(obj)
                anno.recalc()

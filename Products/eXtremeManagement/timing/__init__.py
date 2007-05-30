try:
    import zope.annotation
except ImportError:
    # BBB for Zope 2.9
    import zope.app.annotation
    import zope.app.annotation.interfaces
    import sys
    sys.modules['zope.annotation'] = zope.app.annotation
    sys.modules['zope.annotation.interfaces'] = zope.app.annotation.interfaces

from zope.interface import implements, alsoProvides, classImplements
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable
from persistent.dict import PersistentDict
from Products.CMFPlone import CatalogTool as catalogtool
from Products.eXtremeManagement.timing.interfaces import IActualHours
from Products.eXtremeManagement.timing.interfaces import IEstimate


class ActualHoursContainer(object):
    """An adapter for actual hours containers, like Task.
    """

    implements(IActualHours)
    ANNO_KEY = 'extrememanagement.actual'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.metadata = annotations.get(self.ANNO_KEY, None)
        if self.metadata is None:
            annotations[self.ANNO_KEY] = PersistentDict()
            self.metadata = annotations[self.ANNO_KEY]

    def __get_actual_time(self):
        return self.metadata.get('actual_time', 0.0)
    def __set_actual_time(self, v):
        if not isinstance(v, float):
            v = float(v)
        self.metadata['actual_time'] = v
    actual_time = property(__get_actual_time, __set_actual_time)

    def recalc(self):
        """Recalculate the total booked hours for this container.
        """
        context = self.context
        total = 0.0
        for obj in context.contentValues():
            actual = IActualHours(obj, None)
            if actual is not None:
                total += actual.actual_time
        self.actual_time = total
        context.reindexObject(idxs=['actual_time'])


class EstimateContainer(ActualHoursContainer):
    implements(IEstimate)
    ANNO_KEY = 'extrememanagement.estimate'

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        self.metadata = annotations.get(self.ANNO_KEY, None)
        if self.metadata is None:
            annotations[self.ANNO_KEY] = PersistentDict()
            self.metadata = annotations[self.ANNO_KEY]

    def __get_estimate(self):
        return self.metadata.get('estimate', 0.0)
    def __set_estimate(self, v):
        if not isinstance(v, float):
            v = float(v)
        self.metadata['estimate'] = v
    estimate = property(__get_estimate, __set_estimate)

    def recalc(self):
        """Recalculate the total of estimates for this container.
        """
        context = self.context
        total = 0.0
        for obj in context.contentValues():
            anno = IEstimate(obj, None)
            if anno is not None:
                total += anno.estimate
        self.estimate = total
        context.reindexObject(idxs=['estimate'])


def actual(object, portal, **kw):
    anno = IActualHours(object, None)
    if anno is not None:
        return anno.actual_time
    return None


def estimate(object, portal, **kw):
    anno = IEstimate(object, None)
    if anno is not None:
        return anno.estimate
    return None


catalogtool.registerIndexableAttribute('actual_time', actual)
catalogtool.registerIndexableAttribute('estimate', estimate)

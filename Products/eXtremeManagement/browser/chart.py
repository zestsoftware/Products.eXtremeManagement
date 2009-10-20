from Acquisition import aq_inner
from zope import interface

import string

from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.eXtremeManagement import XMMessageFactory as _

from xm.booking.timing.interfaces import IActualHours, ISizeEstimate, IEstimate

from pygooglechart import SimpleLineChart, Axis, ExtendedData

from plone.memoize.view import memoize


class IChartView(interface.Interface):
    """Interface for charts"""

    def has_data():
        """test to see if there is any data to show"""

    def velocity_chart(self):
        """Draws the ammount of work estimated versus the ammount of work
           done
        """


class ChartView(BrowserView):
    """ Helper view for generating the chart url and if charts are
        available
        Also used for the main chart page on a project """

    def __init__(self, context, request):
        super(ChartView, self).__init__(context, request)
        self.table = []
        self.total_iterations = 0
        self.project = aq_inner(self.context).getProject()
        for it in self.get_iterations_generator():
            self.total_iterations +=1
            estim_total = int(self.get_total_estimate_iteration(it)+0.5)
            estim_total_adapt = int((IEstimate(it).estimate / 8.0) + 0.5)
            work_total = int((IActualHours(it).actual_time / 8.0) + 0.5)
            self.table.append({'label': it.title_or_id(),
                               'estimate_stories': estim_total,
                               'estimate_tasks': estim_total_adapt,
                               'worked': work_total})

    @memoize
    def total_budget(self):
        """ return total budget hours"""
        budgetString = self.project.getBudgetHours()
        if len(string.strip(budgetString))>0:
            return int(float(budgetString)+0.5)
        else:
            return None

    @memoize
    def has_data(self):
        portal_properties = getToolByName(self.context, 'portal_properties')
        xm_props = portal_properties.xm_properties
        if self.context.portal_type == 'Project':
            if (not hasattr(xm_props, 'project_chart')
                or not xm_props.project_chart):
                return False
            return self.total_iterations > 1
        return False

    def get_iterations_generator(self):
        """ return a generator for all iterations having iter in their name"""
        return (i for i in self.context.contentValues()
                if i.portal_type=='Iteration' and
                'iter' in i.title_or_id().lower())

    def get_total_estimate_iteration(self, iteration):
        """ sum of rough story estimates in an iteration """
        #XXX FIX ME, I AM TOO TIME EXPENSIVE
        total = 0.0

        for story in (i for i in iteration.contentValues()
                              if i.portal_type=='Story'):
            if ISizeEstimate.providedBy(story):
                total += ISizeEstimate(story).size_estimate
        return total

### Table & graph data per iteration methods

    @memoize
    def labels(self):
        return [it.title_or_id for it in self.get_iterations_generator()]

    @memoize
    def estimate_stories_data(self):
        """ estimates for all iterations in a project"""
        return [i['estimate_stories'] for i in self.table]

    @memoize
    def estimate_tasks_data(self):
        """ estimates for all iterations in a project"""
        return [i['estimate_tasks'] for i in self.table]

    @memoize
    def work_data(self):
        """ actual hours work in an iteration """
        return [i['worked'] for i in self.table]

    @memoize
    def cumulative_estimate_stories_data(self):
        """ cumulative estimates for all iterations in a project"""
        cumul = []
        done = 0
        for work in self.estimate_stories_data():
            cumul.append(work+done)
            done += work
        return cumul

    @memoize
    def cumulative_work_data(self):
        """ estimates for all iterations in a project"""
        cumul = []
        done = 0
        for work in self.work_data():
            cumul.append(work+done)
            done += work
        return cumul

    def velocity_table(self):
        return zip(self.labels(), self.estimate_stories_data(),
                   self.estimate_tasks_data(), self.work_data())

    def velocity_chart(self):

        graph_width = 600
        graph_height = 300

        x_max = self.total_iterations
        y_max = max(max(self.estimate_stories_data()),
                    max(self.estimate_tasks_data()),
                    max(self.work_data()))

        chart = SimpleLineChart(graph_width, graph_height,
                                x_range=(1, x_max+1), y_range=(0, y_max+1))

        chart.add_data(self.estimate_stories_data())
        chart.add_data(self.estimate_tasks_data())
        chart.add_data(self.work_data())

        chart.set_grid(0, 100.0/y_max+1, 5, 5)
        chart.set_colours(['FF0000', '00FF00', '0000FF'])
        chart.set_legend([ _('rough story estimates'), _('task estimates'), _('worked') ])
        chart.set_legend_position('b')
        chart.set_axis_labels(Axis.LEFT, ['', '', _('days')])
        chart.set_axis_labels(Axis.BOTTOM, range(1, x_max+1))
        chart.set_axis_range(Axis.LEFT, 0, y_max+1)

        return chart.get_url(data_class=ExtendedData)

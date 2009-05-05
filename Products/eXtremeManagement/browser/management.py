from Acquisition import aq_inner, aq_parent
from zope import component
from DateTime import DateTime
import logging

from Products.eXtremeManagement.browser.xmbase import XMBaseView
from Products.eXtremeManagement.utils import formatTime

logger = logging.getLogger('xm.listing')


class IterationListBaseView(XMBaseView):

    iteration_review_state = 'change_in_subclasses'
    billable_only = None
    
    _total = None

    def sort_results(self, results):
        # allow sorting in subclasses
        return results

    def add_to_total(self, iteration_dict):
        """Increase total with this iteration's value"""
        pass

    def extra_dict(self, obj, brain):
        """Add additional information to the iterationdict."""
        return {}

    def projectlist(self):
        context = aq_inner(self.context)
        searchpath = '/'.join(context.getPhysicalPath())
        # By default search for all projects from the given path
        # if the context is a project it will return itself
        cfilter = dict(portal_type='Project',
                       path={'query': searchpath, 'navtree': False})
        if self.billable_only is not None:
            cfilter['getBillableProject'] = self.billable_only
            

        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        portal = portal_state.portal()
        if context == portal:
            cfilter['review_state'] = 'active'
        projectbrains = self.catalog.searchResults(cfilter)
        logger.info('%r projects found to iterate over' % len(projectbrains))

        results = []
        for projectbrain in projectbrains:
            searchpath = projectbrain.getPath()
            # Search for Iterations that are ready to get invoiced
            iterationbrains = self.catalog.searchResults(
                portal_type='Iteration',
                review_state=self.iteration_review_state,
                path={'query': searchpath, 'navtree': False},
                sort_on='getEndDate')
            if len(iterationbrains) > 0:
                iteration_list = []
                for iterationbrain in iterationbrains:
                    info = self.iterationbrain2dict(iterationbrain)
                    self.add_to_total(info)
                    iteration_list.append(info)
                info = self.projectbrain2dict(projectbrain)
                info['iterations'] = self.sort_results(iteration_list)
                results.append(info)
        return results

    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            list(self.projectlist())
        return self._total

    def iterationbrain2dict(self, brain):
        """Get a dict with info from this iteration brain.
        """
        review_state_id = brain.review_state
        estimate = brain.estimate
        actual = brain.actual_time
        obj = brain.getObject()
        history = self.workflow.getHistoryOf('eXtreme_Iteration_Workflow',
                                             obj)
        completion_date = None
        for item in history:
            if item['action'] == 'complete':
                completion_date = item['time']
        end_date = obj.getEndDate()
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
            icon = brain.getIcon,
            man_hours = brain.getManHours,
            raw_estimate = estimate,
            estimate = formatTime(estimate),
            raw_actual = actual,
            actual = formatTime(actual),
            difference = formatTime(estimate - actual),
            review_state = review_state_id,
            review_state_title = self.workflow.getTitleForStateOnType(
                                 review_state_id, 'Iteration'),
            start_date = obj.getStartDate(),
            completion_date = completion_date,
            end_date = end_date,
            brain= brain,
        )
        returnvalue.update(self.extra_dict(obj, brain))
        return returnvalue

    def projectbrain2dict(self, brain):
        """Get a dict with info from this project brain.
        """
        returnvalue = dict(
            url = brain.getURL(),
            title = brain.Title,
            description = brain.Description,
        )
        return returnvalue


class InvoicingView(IterationListBaseView):

    iteration_review_state = 'completed'
    billable_only = True
    _invoiced_total = 0.0

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0
        self._total += iteration_dict['raw_estimate']

    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._total

    def invoiced_total(self):
        if self._invoiced_total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.invoicedlist()
        if self._invoiced_total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._invoiced_total

    def invoicedlist(self):
        """ Return a list on invoiced iterations
        """
        # Search for Iterations that have been invoiced in the past month
        year = DateTime().year()
        month = DateTime().month()
        start_of_month = DateTime(year, month, 1)
        iterationbrains = self.catalog.searchResults(
            portal_type='Iteration',
            review_state='invoiced',
            modified={'query': start_of_month, 'range': 'min'},
            sort_on='getEndDate')
        results = []
        for iterationbrain in iterationbrains:
            iteration_info = self.iterationbrain2dict(iterationbrain)
            self._invoiced_total += float(iterationbrain.estimate)
            project = aq_parent(aq_inner(iterationbrain.getObject()))
            project_info = dict(url = project.absolute_url(),
                                title = project.Title(),
                                description = project.Description())
            project_info['iterations'] = [iteration_info]
            results.append(project_info)
        return results


class InProgressView(IterationListBaseView):
    
    billable = 'billable'
    _actual = 0.0

    def add_to_total(self, iteration_dict):
        if self._total is None:
            self._total = 0.0
        self._total += float(iteration_dict['raw_estimate'])

    def total(self):
        if self._total is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._total is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._total
        
    def total_actual(self):
        if self._actual is None:
            # projectlist hasn't been called yet, so do it to
            # update the total.
            self.projectlist()
        if self._actual is None:
            # total could still be none if there are no iterations.
            return ''
        return '%.2f' % self._actual
    
    def viewing_billable(self):
        btype = self.request.get('type', 'billable')
        if btype == 'unbillable':
            return False
        return True

    def unbillable_url(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        return portal_state.portal_url() + '/inprogress?type=unbillable'

    def billable_url(self):
        portal_state = component.getMultiAdapter((self.context, self.request),
                                                 name=u'plone_portal_state')
        return portal_state.portal_url() + '/inprogress?type=billable'

    def projectlist(self):
        """ Return a list on invoiced iterations
        """
        self.billable = self.request.get('type', 'billable')
        cfilter = dict(portal_type = 'Iteration',
                       review_state = 'in-progress',
                       getBillableProject = self.viewing_billable(),
                       sort_on = 'getEndDate')
        iterationbrains = self.catalog.searchResults(cfilter)
        results = []
        for iterationbrain in iterationbrains:
            iteration_info = self.iterationbrain2dict(iterationbrain)
            self.add_to_total(iteration_info)
            self._actual += iteration_info['raw_actual']
            project = aq_parent(aq_inner(iterationbrain.getObject()))
            project_info = dict(url = project.absolute_url(),
                                title = project.Title(),
                                description = project.Description())
            project_info['iterations'] = [iteration_info]
            results.append(project_info)
        return results

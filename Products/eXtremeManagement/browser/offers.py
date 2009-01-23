from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName

from Products.eXtremeManagement.browser.iterations import IterationView
from Products.eXtremeManagement.utils import getStateSortedContents


class OfferView(IterationView):
    """Return information about an offer.
    """

    def show_draft(self):
        """Return whether draft state of stories should be shown in the view.
        """
        context = aq_inner(self.context)
        return context.get('show_draft', False)

    def stories(self):
        """Return the Stories of this Offer.
        """
        show_draft = self.show_draft()
        context = aq_inner(self.context)
        filter = dict(portal_type='Story',
                      sort_on='getObjPositionInParent')
        items = context.getFolderContents(filter)
        storybrains = getStateSortedContents(items)

        story_list = []

        membership = getToolByName(context, 'portal_membership')

        for storybrain in storybrains:
            story_obj = storybrain.getObject()
            review_state = storybrain.review_state
            is_draft = review_state == 'draft'
            if is_draft and show_draft:
                draft_class = 'state-draft'
            else:
                draft_class = ''
            editable = (membership.checkPermission('Modify portal content',
                                                   story_obj)
                or membership.checkPermission(
                    'eXtremeManagement: Edit roughEstimate', story_obj))
            story = dict(
                story_id = storybrain.getId,
                title = storybrain.Title,
                url = storybrain.getURL(),
                main_text = story_obj.getMainText(),
                story_obj = story_obj,
                size_estimate = storybrain.size_estimate,
                review_state = review_state,
                review_state_title = self.workflow.getTitleForStateOnType(
                    review_state, 'Story'),
                show_draft_story = show_draft and is_draft,
                draft_class = draft_class,
                editable = editable,
                )
            story_list.append(story)
        return story_list

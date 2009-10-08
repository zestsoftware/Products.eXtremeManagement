# Utilities for the testbrowser tests.


def login(browser, portal, username):
    browser.open(portal.absolute_url() + '/login_form')
    browser.getLink('Log in').click()
    browser.getControl(name='__ac_name').value = username
    browser.getControl(name='__ac_password').value = 'secret'
    browser.getControl(name='submit').click()
    if 'You are now logged in' not in browser.contents:
        return 'login failed'


def logout(browser, portal):
    browser.open(portal.absolute_url())
    browser.getLink('Log out').click()


def _submitChecks(browser, title):
    if title not in browser.contents:
        return 'title not in browser.contents'
    if 'Changes saved.' not in browser.contents:
        return 'Changes on edit form not saved.'


def addSimpleType(browser, container, title, type_name):
    """Add a content type with just a title.
    """
    browser.open(
        container.absolute_url() + '/createObject?type_name=' + type_name)
    browser.getControl(name='title').value = title
    try:
        button = browser.getControl(name='form.button.save')
    except LookupError:
        # BBB for Plone < 3.3 (Products.Archetypes < 1.5.11)
        button = browser.getControl(name='form_submit')
    button.click()
    return _submitChecks(browser, title)


# BBB Can be removed in release 2.1
def addProjectFolder(browser, container, title):
    """Add a ProjectFolder
    """
    return addSimpleType(browser, container, title, 'ProjectFolder')


def addProject(browser, container, title):
    """Add a Project.
    """
    return addSimpleType(browser, container, title, 'Project')


def addIteration(browser, container, title):
    """Add an Iteration.
    """
    return addSimpleType(browser, container, title, 'Iteration')


def addOffer(browser, container, title):
    """Add an Offer.
    """
    return addSimpleType(browser, container, title, 'Offer')


def addStory(browser, container, title, text, estimate=None):
    """Add a Story.
    """
    browser.open(container.absolute_url() + '/createObject?type_name=Story')
    browser.getControl(name='title').value = title
    browser.getControl(name='mainText').value = text
    if estimate is not None:
        browser.getControl(name='roughEstimate').value = str(estimate)
    try:
        button = browser.getControl(name='form.button.save')
    except LookupError:
        # BBB for Plone < 3.3 (Products.Archetypes < 1.5.11)
        button = browser.getControl(name='form_submit')
    button.click()
    return _submitChecks(browser, title)


def addTask(browser, container, title):
    """Add a Task.
    """
    return addSimpleType(browser, container, title, 'Task')


def addBooking(browser, container, title, hours=None, minutes=None):
    """Add a Booking
    """
    browser.open(container.absolute_url() + '/createObject?type_name=Booking')
    browser.getControl(name='title').value = title
    if hours is not None:
        browser.getControl(name='hours').value = [str(hours)]
    if minutes is not None:
        browser.getControl(name='minutes').value = [str(minutes)]
    try:
        button = browser.getControl(name='form.button.save')
    except LookupError:
        # BBB for Plone < 3.3 (Products.Archetypes < 1.5.11)
        button = browser.getControl(name='form_submit')
    button.click()
    return _submitChecks(browser, title)


def transition(browser, object, transition):
    browser.open(object.absolute_url())
    browser.getLink(transition).click()
    if "Your content's status has been modified." not in browser.contents and \
       "<dd>Item state changed.</dd>" not in browser.contents:
        return 'Transition failed.'

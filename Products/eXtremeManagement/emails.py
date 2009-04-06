import logging
from email.MIMEText import MIMEText
from email.Header import Header
from email.Utils import parseaddr, formataddr
from socket import gaierror

from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import safe_unicode

from xm.booking.timing.interfaces import IEstimate

logger = logging.getLogger("xm emails")


def email_address_for_member(member):
    """Return a formatted fullname plus email address for this member.

    We create a fake Member class for testing:

    >>> class Member(object):
    ...     def __init__(self, fullname='', email=''):
    ...         self.fullname = fullname
    ...         self.email = email
    ...     def getProperty(self, propname, default=None):
    ...         if propname == 'fullname':
    ...             return self.fullname
    ...         if propname == 'email':
    ...             return self.email
    ...         return default

    We define an alias for this function to make the line shorter:

    >>> efm = email_address_for_member

    Now we do some tests:

    >>> efm(None)
    ''
    >>> efm(Member())
    ''
    >>> efm(Member(fullname='Maurits van Rees'))
    ''
    >>> efm(Member(email='a@b.c'))
    'a@b.c'
    >>> efm(Member('Maurits van Rees', 'a@b.c'))
    'Maurits van Rees <a@b.c>'

    The parseaddr function can get confused in the face of special
    characters, which leads to misinterpreting the email address.  I
    saw that in the browser, but could not find a way to create a test
    for that.  Anyway, in case of confusion we just return the email
    address and not the fullname.

    """
    if not member:
        # Maybe a test user?
        return ''

    email = member.getProperty('email', '')
    if not email:
        return ''
    fullname = member.getProperty('fullname', '')

    formatted = formataddr((fullname, email))
    if parseaddr(formatted)[1] != email:
        # formataddr probably got confused by special characters.
        return email
    return formatted


def send(portal, message, subject, recipients=[]):
    """Send an email.

    Partly taken from plonehrm.notifications.emailer.

    This takes some hints from
    http://mg.pov.lt/blog/unicode-emails-in-python.html

    The charset of the email will be the first one out of US-ASCII,
    the email_charset set in the properties of the portal (or
    ISO-8859-1) and UTF-8 that can represent all the characters
    occurring in the email.
    """
    # Weed out any empty strings.
    recipients = [r for r in recipients if r]
    if not recipients:
        logger.warn("No recipients to send the mail to, not sending.")
        return

    charset = portal.getProperty('email_charset', 'ISO-8859-1')
    # Header class is smart enough to try US-ASCII, then the charset we
    # provide, then fall back to UTF-8.
    header_charset = charset

    # We must choose the body charset manually
    for body_charset in 'US-ASCII', charset, 'UTF-8':
        try:
            message = message.encode(body_charset)
        except UnicodeError:
            pass
        else:
            break

    # Get the 'From' address.
    sender_name = portal.getProperty('email_from_name')
    sender_addr = portal.getProperty('email_from_address')

    # We must always pass Unicode strings to Header, otherwise it will
    # use RFC 2047 encoding even on plain ASCII strings.
    sender_name = str(Header(safe_unicode(sender_name), header_charset))
    # Make sure email addresses do not contain non-ASCII characters
    sender_addr = sender_addr.encode('ascii')
    # XXX We should first format the address, and *then* use the
    # Header class.
    email_from = formataddr((sender_name, sender_addr))

    # Same for the list of recipients.
    """
    #For testing...
    recipients = [formataddr(('Maurits van Rees',
                              'maurits@vanrees.org')),
                  formataddr(('Maurits van Rees 2',
                              'maurits+2@vanrees.org'))]
    """
    formatted_recipients = []
    for recipient in recipients:
        # Split real name (which is optional) and email address parts
        recipient_name, recipient_addr = parseaddr(recipient)
        recipient_name = str(Header(safe_unicode(recipient_name),
                                    header_charset))
        recipient_addr = recipient_addr.encode('ascii')
        # XXX We should first format the address, and *then* use the
        # Header class.
        formatted = formataddr((recipient_name, recipient_addr))
        formatted_recipients.append(formatted)
    email_to = ', '.join(formatted_recipients)

    # Make the subject a nice header
    subject = Header(safe_unicode(subject), header_charset)

    # Create the message ('plain' stands for Content-Type: text/plain)
    msg = MIMEText(message, 'plain', body_charset)
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = subject
    msg = msg.as_string()

    # Finally send it out.
    mailhost = getToolByName(portal, 'MailHost')
    try:
        logger.info("Begin sending email to %r " % formatted_recipients)
        logger.info("Subject: %s " % subject)
        mailhost.send(message=msg)
    except gaierror, exc:
        logger.error("Failed sending email to %r" % formatted_recipients)
        logger.error("Reason: %s: %r" % (exc.__class__.__name__, str(exc)))
    else:
        logger.info("Succesfully sent email to %r" % formatted_recipients)


def email_task_assignees(object, event, *args, **kwargs):
    # First some sanity checks.
    if event.new_state.id != 'to-do':
        return
    if not object is event.object:
        # This is in case an event is sent to the parent as well,
        # which at least happens for some events.
        return
    portal = getToolByName(object, 'portal_url').getPortalObject()
    portal_properties = getToolByName(portal, 'portal_properties')
    xm_props = portal_properties.xm_properties
    if not xm_props.send_task_mails:
        return

    membership = getToolByName(portal, 'portal_membership')
    creator = membership.getMemberById(object.Creator())
    member_id = membership.getAuthenticatedMember().id
    creator_address = email_address_for_member(creator)
    title = object.Title()
    subject = u'New Task assigned: %s' % safe_unicode(title)
    obj_url = object.absolute_url()
    description = object.Description()
    if description:
        # XXX There are ideas to not use the description anymore on
        # Tasks and only use the main text.
        description = 'The description of the task is:\n' + description

    estimate = IEstimate(object, None)
    if estimate is not None:
        estimate = estimate.hours
    recipients = [email_address_for_member(membership.getMemberById(a))
                  for a in object.getAssignees() if a != member_id]

    # Let's make sure all strings are unicode.
    values = dict(
        task_url = safe_unicode(obj_url),
        creator = safe_unicode(creator_address),
        description = safe_unicode(description),
        estimate = estimate)

    message = email_task_assignees_template % values
    logger.info(message)
    send(portal, message, subject, recipients)


email_task_assignees_template = u"""
The url is:
%(task_url)s

The original creator of this task is:
%(creator)s

%(description)s

This estimate for this task is currently: %(estimate)r hours.

You can do it!
"""

import logging
log = logging.getLogger("eXtremeManagement")
log.debug('Start initialization of product.')

from zope.i18nmessageid import MessageFactory
XMMessageFactory = MessageFactory('eXtremeManagement')
from Products.CMFCore import utils as cmfutils
from Products.Archetypes.atapi import process_types
from Products.Archetypes import listTypes

from Products.eXtremeManagement import config


def initialize(context):
    # imports packages and types for registration
    import content
    import interfaces

    # Initialize portal content
    all_content_types, all_constructors, all_ftis = process_types(
        listTypes('eXtremeManagement'),
        'eXtremeManagement')

    cmfutils.ContentInit(
        'eXtremeManagement Content',
        content_types = all_content_types,
        permission = config.DEFAULT_ADD_CONTENT_PERMISSION,
        extra_constructors = all_constructors,
        fti = all_ftis,
        ).initialize(context)

    # Give it some extra permissions to control them on a per class limit
    for i in range(0, len(all_content_types)):
        klassname=all_content_types[i].__name__
        if not klassname in config.ADD_CONTENT_PERMISSIONS:
            continue

        context.registerClass(
            meta_type = all_ftis[i]['meta_type'],
            constructors = (all_constructors[i], ),
            permission = config.ADD_CONTENT_PERMISSIONS[klassname])

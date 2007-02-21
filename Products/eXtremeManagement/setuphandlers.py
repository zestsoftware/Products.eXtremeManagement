def reindexIndexes(site):
    """Reindex some indexes.

    Indexes that are added in the catalog.xml file get cleared
    everytime the GenericSetup profile is applied.  So we need to
    reindex them.

    Since we are forced to do that, we might as well make sure that
    these get reindexed in the correct order.  At least id *might*
    help for some of the indexes for estimates and booked hours to be
    reindexed in a specific order.
    """
    cat = site.portal_catalog
    indexes = [
        'getAddress',
        'getAssignees',
        'getBookingDate',
        'getCity',
        'getCountry',
        'getEmail',
        'getFax',
        'getFullname',
        'getHours', # before getRawActualHours, getRawEstimate and
                    # getRawDifference
        'getMinutes', # before getRawActualHours, getRawEstimate and
                      # getRawDifference
        'getName',
        'getPhone',
        'getRawActualHours',
        'getRawEstimate',
        'getEstimate', # after getRawEstimate
        'getRawDifference', # after getRawActualHours and getRawEstimate
        'getRawRelatedItems',
        'getWebsite',
        'getZipCode',
        ]
    # Don't reindex an index if it isn't actually in the catalog.
    # Should not happen, but cannot do any harm.
    ids = [id for id in indexes if id in cat.indexes()]
    if ids:
        cat.manage_reindexIndex(ids=ids)
        

def importVarious(context):
    site = context.getSite()
    reindexIndexes(site)

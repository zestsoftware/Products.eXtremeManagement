# /bin/bash

# Project name
PROJECT=eXtremeManagement

# Find i18n attributes in these files:
# Ignore booking_year.pt for now, as i18ndude does not like it.
# Browser views can help there.
# Also ignore xm_dashboard.pt as that has too many errors according to
# i18ndude, and I do not use it currently.
TEMPLATE_FILES=$(find . -name booking_year.pt -prune -o -name xm_dashboard.pt -prune -o -name '*pt' -print)
# Directory that will be search for i18n tags, including subdirs.
SEARCH_DIR=.
# Merge the contents of this file into the i18n created file.
SELF_MADE=i18n/generated.pot

# Rebuild the .pot file of our project and merge the $SELF_MADE file in it.
#i18ndude rebuild-pot --pot i18n/$PROJECT.pot --create $PROJECT --merge $SELF_MADE $TEMPLATE_FILES
i18ndude rebuild-pot --pot i18n/$PROJECT.pot --create $PROJECT --merge $SELF_MADE $SEARCH_DIR
# Instead of $TEMPLATE_FILES you could use $SEARCH_DIR.

i18ndude sync --pot i18n/$PROJECT.pot i18n/$PROJECT-*.po

i18ndude sync --pot i18n/plone.pot i18n/plone-$PROJECT-*.po


echo "Reporting some statistics..."
# Find places that are missing an "i18n:translate" or
# "i18n:attributes" tag.
i18ndude find-untranslated  $TEMPLATE_FILES

echo "Percentage done per language:"
i18ndude chart -o /dev/null --pot i18n/$PROJECT.pot i18n/$PROJECT-*.po

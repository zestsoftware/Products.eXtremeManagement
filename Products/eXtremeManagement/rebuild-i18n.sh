# /bin/sh

# Project name
PROJECT=eXtremeManagement
# Find i18n attributes in these files:
TEMPLATE_FILES=$(find -name '*pt')
# Directory that will be search for i18n tags, including subdirs.
SEARCH_DIR=skins/$PROJECT
# Merge the contents of this file into the i18n created file.
SELF_MADE=i18n/generated.pot

# Rebuild the .pot file of our project and merge the $SELF_MADE file in it.
i18ndude rebuild-pot --pot i18n/$PROJECT.pot --create $PROJECT --merge $SELF_MADE $SEARCH_DIR

i18ndude sync --pot i18n/$PROJECT.pot i18n/$PROJECT-*.po

echo "Reporting some statistics..." 
# Find places that are missing an "i18n:translate" or
# "i18n:attributes" tag.
i18ndude find-untranslated -s $TEMPLATE_FILES

echo "Percentage done per language:"
i18ndude chart -o /dev/null --pot i18n/$PROJECT.pot i18n/$PROJECT-*.po 

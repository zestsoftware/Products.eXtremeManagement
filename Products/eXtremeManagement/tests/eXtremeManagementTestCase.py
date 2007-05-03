import os, sys, code
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from Testing import ZopeTestCase
from Products.PloneTestCase import PloneTestCase
from Products.eXtremeManagement.config import HAS_PLONE21
from Products.eXtremeManagement.config import PRODUCT_DEPENDENCIES
from Products.eXtremeManagement.config import DEPENDENCIES

# Add common dependencies
if not HAS_PLONE21:
    DEPENDENCIES.append('Archetypes')
    PRODUCT_DEPENDENCIES.append('MimetypesRegistry')
    PRODUCT_DEPENDENCIES.append('PortalTransforms')
PRODUCT_DEPENDENCIES.append('eXtremeManagement')

# Install all (product-) dependencies, install them too
for dependency in PRODUCT_DEPENDENCIES + DEPENDENCIES:
    ZopeTestCase.installProduct(dependency)

ZopeTestCase.installProduct('eXtremeManagement')

PRODUCTS = list()
PRODUCTS += DEPENDENCIES
PRODUCTS.append('eXtremeManagement')
testcase = PloneTestCase.PloneTestCase
PloneTestCase.setupPloneSite(products=PRODUCTS)


class eXtremeManagementTestCase(testcase):
    """Base TestCase for eXtremeManagement."""

    def interact(self, locals=None):
        """Provides an interactive shell aka console inside your testcase.

        It looks exact like in a doctestcase and you can copy and paste
        code from the shell into your doctest. The locals in the testcase are
        available, becasue you are in the testcase.

        In your testcase or doctest you can invoke the shell at any point by
        calling::

            >>> self.interact( locals() )

        locals -- passed to InteractiveInterpreter.__init__()
        """
        savestdout = sys.stdout
        sys.stdout = sys.stderr
        sys.stderr.write('='*70)
        console = code.InteractiveConsole(locals)
        console.interact("""
ZopeTestCase Interactive Console
(c) BlueDynamics Alliance, Austria - 2005

Note: You have the same locals available as in your test-case.
""")
        sys.stdout.write('\nend of ZopeTestCase Interactive Console session\n')
        sys.stdout.write('='*70+'\n')
        sys.stdout = savestdout

def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(eXtremeManagementTestCase))
    return suite

if __name__ == '__main__':
    framework()

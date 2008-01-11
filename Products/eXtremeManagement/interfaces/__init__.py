import IXMCustomer as IXMCustomerZope2
from xmcustomerfolder import IXMCustomerFolder
from xmcustomer import IXMCustomer
from xmprojectmember import IXMProjectMember
from xmprojectfolder import IXMProjectFolder
from xmproject import IXMProject
from xmiteration import IXMIteration
from xmoffer import IXMOffer
from xmstory import IXMStory
from xmtask import IXMTask
from xmtask import IIssueTask
from xmbooking import IXMBooking

our_interfaces = (
    IXMCustomerFolder,
    IXMCustomer,
    IXMProjectMember,
    IXMProjectFolder,
    IXMProject,
    IXMIteration,
    IXMOffer,
    IXMStory,
    IXMTask,
    IIssueTask,
    IXMBooking,
    )

from zope.interface import alsoProvides
from zope.app.content.interfaces import IContentType

for iface in our_interfaces:
    alsoProvides(iface, IContentType)

# Only add zope 3 bridges if you somehow need them.
# If this gets removed by someone who knows what he is doing, that is
# fine with me.  [Maurits.]
from Interface.bridge import createZope3Bridge
createZope3Bridge(IXMCustomer, IXMCustomerZope2,
                  'IXMCustomer')


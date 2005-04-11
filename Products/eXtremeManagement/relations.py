from Products.Archetypes.ReferenceEngine import Reference, ReferenceException
from Products.CMFCore.utils import getToolByName

class CustomerProjectRelation(Reference):
    relationship = 'CustProjRelation'



## Script (Python) "update_hours"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Update the actual hours on open tasks
##

REQUEST = context.REQUEST

originals = {}
entered   = {}

for key in REQUEST.keys():
    if key.startswith('actual-'):
        actual=REQUEST[key]
        if key.startswith('actual-original-'):
            id=key[len('actual-original-'):]
            originals[id]=actual
        if key.startswith('actual-entered-'):
            id=key[len('actual-entered-'):]
            entered[id]=actual

return originals 

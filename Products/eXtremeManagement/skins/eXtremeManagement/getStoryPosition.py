## Script (Python) "getStoryPosition"
##title=Return the index of the current Story
##parameters=obj=None,stories=None

for i in range(len(stories)):
    if stories[i].getId() == obj.getId():
        return i
return None


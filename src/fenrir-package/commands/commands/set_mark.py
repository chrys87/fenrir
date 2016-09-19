#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'places marks to select text to copy to the clipboard'        
    
    def run(self, environment):
        if environment['screenData']['newCursorReview'] == None:
            environment['runtime']['outputManager'].presentText(environment, 'no review cursor', interrupt=True)
            return

        if environment['commandBuffer']['Marks']['1'] == None:
            environment['commandBuffer']['Marks']['1'] = environment['screenData']['newCursorReview'].copy()
        else:
            if environment['commandBuffer']['Marks']['2'] == None:
                environment['commandBuffer']['Marks']['2'] = environment['screenData']['newCursorReview'].copy()
            else:
                environment['commandBuffer']['Marks']['3'] = environment['screenData']['newCursorReview'].copy()

        environment['runtime']['outputManager'].presentText(environment, 'set mark', interrupt=True)
 
    def setCallback(self, callback):
        pass

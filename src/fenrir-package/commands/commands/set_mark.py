#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment 
    def getDescription(self):
        return 'No Description found'        
    def run(self, environment):
        if environment['screenData']['newCursorReview'] == None:
            environment['runtime']['outputManager'].presentText(environment, 'no review cursor', interrupt=True)
            return environment   

        if environment['commandBuffer']['Marks']['1'] == None:
            environment['commandBuffer']['Marks']['1'] = environment['screenData']['newCursorReview'].copy()
        else:
            if environment['commandBuffer']['Marks']['2'] == None:
                environment['commandBuffer']['Marks']['2'] = environment['screenData']['newCursorReview'].copy()
            else:
                environment['commandBuffer']['Marks']['3'] = environment['screenData']['newCursorReview'].copy()

        environment['runtime']['outputManager'].presentText(environment, 'set mark', interrupt=True)

        return environment          
    def setCallback(self, callback):
        pass

#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newCursorReview'] == None:
            environment['runtime']['outputManager'].presentText(environment, 'no review cursor', interrupt=True)

        if environment['commandBuffer']['Marks']['1'] == None:
            environment['commandBuffer']['Marks']['1'] = environment['screenData']['newCursorReview']
        else:
            environment['commandBuffer']['Marks']['2'] = environment['screenData']['newCursorReview']

        environment['runtime']['outputManager'].presentText(environment, 'set mark', interrupt=True)
        return environment                
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

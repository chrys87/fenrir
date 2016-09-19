#!/bin/python

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return 'exits review mode'        
    
    def run(self, environment):
        if (environment['screenData']['oldCursorReview'] == None) and \
          (environment['screenData']['newCursorReview'] == None):
            environment['runtime']['outputManager'].presentText(environment, "Not in review mode", interrupt=True)
            return  

        environment['screenData']['oldCursorReview'] = None
        environment['screenData']['newCursorReview'] = None
        environment['runtime']['outputManager'].presentText(environment, "leve review mode", interrupt=True)
   
    def setCallback(self, callback):
        pass

#!/bin/python
import time
class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getDescription(self, environment):
        return ''          
    
    def run(self, environment):
        # TTY Change
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
        if environment['runtime']['inputManager'].noKeyPressed(environment):
            return            
        # detect an change on the screen, we just want to cursor arround, so no change should appear
        if environment['screenData']['newDelta'] != '':
            return
        if environment['screenData']['newNegativeDelta'] != '':
            return            
        # is it a horizontal change?
        if environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y'] or\
          environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x']:
            return
        print('drin')
        if environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']].strip() == '':
            pass
            #environment['runtime']['outputManager'].presentText(environment, "blank",True)
        else:
            environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']],interrupt=True)
 
    def setCallback(self, callback):
        pass


#!/bin/python

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
        if environment['screenData']['newTTY'] != environment['screenData']['oldTTY']:
            return
        if environment['screenData']['newDelta'] != environment['screenData']['oldDelta']:
            return    
        if environment['screenData']['newCursor']['y'] == environment['screenData']['oldCursor']['y']:
            return
        currLine = environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']]
        if currLine.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, currLine, interrupt=True)
 
    def setCallback(self, callback):
        pass


#!/bin/python
import time
class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['screenData']['newCursor']['y'] != environment['screenData']['oldCursor']['y'] or\
          environment['screenData']['newCursor']['x'] == environment['screenData']['oldCursor']['x']:
            return environment
        if environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']].replace(" ","").replace("\n","").replace("\t","") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank",True)
        else:
            environment['runtime']['outputManager'].presentText(environment, environment['screenData']['newContentText'].split('\n')[environment['screenData']['newCursor']['y']][environment['screenData']['newCursor']['x']],True)

        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

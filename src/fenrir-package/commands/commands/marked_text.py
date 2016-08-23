#!/bin/python
from utils import mark_utils

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if (environment['commandBuffer']['Marks']['1'] == None) or \
          (environment['commandBuffer']['Marks']['2'] == None):
            environment['runtime']['outputManager'].presentText(environment, "two marks needed", interrupt=True)
            return environment
        
        marked = mark_utils.getTextBetweenMarks(environment['commandBuffer']['Marks']['1'], environment['commandBuffer']['Marks']['2'], environment['screenData']['newContentText'].split('\n'))
        print(marked)
        if marked.strip(" \t\n") == '':
            environment['runtime']['outputManager'].presentText(environment, "blank", soundIcon='EmptyLine', interrupt=True)
        else:
            environment['runtime']['outputManager'].presentText(environment, marked, interrupt=True)
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

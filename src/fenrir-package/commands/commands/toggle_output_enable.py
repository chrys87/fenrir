#!/bin/python

class command():
    def __init__(self):
        pass
    def run(self, environment):
        if environment['speech']['enabled'] or \
          environment['sound']['enabled'] or \
          environment['braille']['enabled']:
            environment['runtime']['outputManager'].presentText(environment, "fenrir muted")          
            environment['speech']['enabled'] = False
            environment['sound']['enabled'] = False
            environment['braille']['enabled'] = False
        else:
            environment['runtime']['outputManager'].presentText(environment, "fenrir unmuted")           
            environment['speech']['enabled'] = True
            environment['sound']['enabled'] = True
            environment['braille']['enabled'] = True
        return environment    
    def setCallback(self, callback):
        pass
    def shutdown(self):
        pass

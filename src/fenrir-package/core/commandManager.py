#!/bin/python

class commandManager():
    def __init__(self):
        pass
    def loadCommands(self, environment):
        return environment
    def executeCommand(self, environment):
        print(environment['commandInfo']['currCommand'])
        if self.isCommandDefined(environment):
            try:
                environ =  environment['commands'][environment['commandInfo']['currCommand']].run(environment)
                if environ != None:
                    environment = environ
            exept: 
                pass
        environment['commandInfo']['currCommand'] = ''
        return environment
        
    def executeNextCommand(self, environment):
        pass
    def isShortcutDefined(self, environment):
        return( environment['input']['currShortcutString'] in environment['bindings'])

    def getCommandForShortcut(self, environment):
        if not self.isShortcutDefined(environment):
            return environment 
        environment['commandInfo']['currCommand'] = environment['bindings'][environment['input']['currShortcutString']]
        return environment

    def isCommandDefined(self, environment):
        return( environment['commandInfo']['currCommand'] in environment['commands'])

    def enqueueCommand(self, environment):
        if not self.isCommandDefined(environment):
            return False
        return True

#!/bin/python
import importlib.util
import glob
import os

class commandManager():
    def __init__(self):
        pass
    def loadCommands(self, environment):
        commandFolder = "commands/"
        commandList = glob.glob(commandFolder+'*')
        for currCommand in commandList:
            try:
                fileName, fileExtension = os.path.splitext(currCommand)
                fileName = fileName.split('/')[-1]
                if fileName in ['__init__','__pycache__']:
                    continue
                print(fileName)
                if fileExtension.lower() == 'py':
                    spec = importlib.util.spec_from_file_location(fileName, currCommand)
                    command_mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(command_mod)
                    environment['commands']['fileName'] = command_mod()
            except:
                continue
        return environment

    def executeCommand(self, environment):
        print(environment['commandInfo']['currCommand'])
        if self.isCommandDefined(environment):
            try:
                environ =  environment['commands'][environment['commandInfo']['currCommand']].run(environment)
                if environ != None:
                    environment = environ
            except: 
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

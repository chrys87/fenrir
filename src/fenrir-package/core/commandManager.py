#!/bin/python
import importlib.util
import glob
import os
import time

class commandManager():
    def __init__(self):
        pass

    def loadCommands(self, environment, section='commands'):
        commandFolder = "commands/" + section +"/"
        commandList = glob.glob(commandFolder+'*')
        for currCommand in commandList:
            try:
                fileName, fileExtension = os.path.splitext(currCommand)
                fileName = fileName.split('/')[-1]
                if fileName in ['__init__','__pycache__']:
                    continue
                if fileExtension.lower() == '.py':
                    spec = importlib.util.spec_from_file_location(fileName, currCommand)
                    command_mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(command_mod)
                    environment['commands'][section][fileName] = command_mod.command()
            except:
                continue
        return environment
    def executeTriggerCommands(self, environment, trigger):
        for cmd in sorted(environment['commands'][trigger]):
            environment = environment['commands'][trigger][cmd].run(environment)
        return environment

    def executeCommand(self, environment, currCommand, section = 'commands'):
        if self.isCommandDefined(environment):
            try:
                environ =  environment['commands'][section][currCommand].run(environment)
                if environ != None:
                    environment = environ
            except: 
                pass
        environment['commandInfo']['currCommand'] = ''
        environment['commandInfo']['lastCommandTime'] = time.time()    
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
        return( environment['commandInfo']['currCommand'] in environment['commands']['commands'])

    def enqueueCommand(self, environment):
        if not self.isCommandDefined(environment):
            return False
        return True

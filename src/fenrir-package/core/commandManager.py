#!/bin/python
import importlib.util
import glob
import os
import time
from utils import debug

class commandManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
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
                    environment['commands'][section][fileName].initialize(environment)
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while loading command:" + currCommand ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)                
                continue
        return environment

    def executeTriggerCommands(self, environment, trigger):
        if environment['runtime']['screenManager'].isSuspendingScreen(environment) :
            return environment
        for cmd in sorted(environment['commands'][trigger]):
            try:
               environ = environment['commands'][trigger][cmd].run(environment)
               if environ != None:
                    environment = environ
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while executing trigger:" + trigger + "." + cmd ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        return environment

    def executeCommand(self, environment, currCommand, section = 'commands'):
        if environment['generalInformation']['suspend']:
            return environment        
        if self.isCommandDefined(environment):
            try:
                environ =  environment['commands'][section][currCommand].run(environment)
                if environ != None:
                    environment = environ
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while executing command:" + section + "." + currCommand ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        environment['commandInfo']['currCommand'] = ''
        environment['commandInfo']['lastCommandTime'] = time.time()    
        return environment

    def isShortcutDefined(self, environment, currShortcutString):
        return( currShortcutString in environment['bindings'])

    def setCurrCommandForExec(self, environment, currCommand):
        environment['commandInfo']['currCommand'] = currCommand
        return environment
        
    def getCommandForShortcut(self, environment, currShortcutString):
        if not self.isShortcutDefined(environment, currShortcutString):
            return '' 
        return environment['bindings'][currShortcutString]

    def isCommandDefined(self, environment, currCommand):
        return( currCommand in environment['commands']['commands'])


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
        environment['runtime']['commandManager'].loadCommands(environment,'commands')
        environment['runtime']['commandManager'].loadCommands(environment,'onInput')
        environment['runtime']['commandManager'].loadCommands(environment,'onScreenChanged')    
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
        if environment['runtime']['screenManager'].isSuspendingScreen(environment):
            return environment
        for cmd in sorted(environment['commands'][trigger]):
            try:
               environment['commands'][trigger][cmd].run(environment)
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while executing trigger:" + trigger + "." + cmd ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        return environment

    def executeCommand(self, environment, currCommand, section = 'commands'):
        if environment['runtime']['screenManager'].isSuspendingScreen(environment) :
            return environment    
        if self.isCommandDefined(environment):
            try:
                environment['commands'][section][currCommand].run(environment)
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while executing command:" + section + "." + currCommand ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        environment['commandInfo']['currCommand'] = ''
        environment['commandInfo']['lastCommandExecutionTime'] = time.time()    
        return environment

    def isShortcutDefined(self, environment, shortcut):
        return( str(shortcut).upper() in environment['bindings'])

    def setCurrCommandForExec(self, environment, currCommand):
        environment['commandInfo']['currCommand'] = currCommand
        return environment


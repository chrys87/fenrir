#!/bin/python
import importlib.util
import glob, os, time
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
        for command in commandList:
            try:
                fileName, fileExtension = os.path.splitext(command)
                fileName = fileName.split('/')[-1]
                if fileName in ['__init__','__pycache__']:
                    continue
                if fileExtension.lower() == '.py':
                    spec = importlib.util.spec_from_file_location(fileName, command)
                    command_mod = importlib.util.module_from_spec(spec)
                    spec.loader.exec_module(command_mod)
                    environment['commands'][section][fileName.upper()] = command_mod.command()
                    environment['commands'][section][fileName.upper()].initialize(environment)
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while loading command:" + command ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)                
                continue
        return environment

    def executeTriggerCommands(self, environment, trigger):
        if environment['runtime']['screenManager'].isSuspendingScreen(environment):
            return environment
        for command in sorted(environment['commands'][trigger]):
            if self.commandExists(environment, command, trigger):        
                try:
                   environment['commands'][trigger][command].run(environment)
                except Exception as e:
                    print(e)
                    environment['runtime']['debug'].writeDebugOut(environment,"Error while executing trigger:" + trigger + "." + cmd ,debug.debugLevel.ERROR)
                    environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        return environment

    def executeCommand(self, environment, command, section = 'commands'):
        if environment['runtime']['screenManager'].isSuspendingScreen(environment) :
            return environment    
        if self.commandExists(environment, command, section):
            try:
                if environment['generalInformation']['tutorialMode']:
                    environment['commands'][section][command].getDescription()
                else:    
                    environment['commands'][section][command].run(environment)
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Error while executing command:" + section + "." + command ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        environment['commandInfo']['currCommand'] = ''
        environment['commandInfo']['lastCommandExecutionTime'] = time.time()    
        return environment

    def isCommandQueued(self, environment):
        return environment['commandInfo']['currCommand'] != ''
        
    def queueCommand(self, environment, command):
        environment['commandInfo']['currCommand'] = command
        return environment
        
    def commandExists(self, environment, command, section = 'commands'):
        return( command.upper() in environment['commands'][section]) 

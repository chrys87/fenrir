#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import importlib.util
import glob, os, time
from core import debug

class commandManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        environment['runtime']['commandManager'].loadCommands(environment,'commands')
        environment['runtime']['commandManager'].loadCommands(environment,'onInput')
        environment['runtime']['commandManager'].loadCommands(environment,'onScreenChanged')    

    def shutdown(self, environment):
        environment['runtime']['commandManager'].shutdownCommands(environment,'commands')
        environment['runtime']['commandManager'].shutdownCommands(environment,'onInput')
        environment['runtime']['commandManager'].shutdownCommands(environment,'onScreenChanged')    
        
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
                environment['runtime']['debug'].writeDebugOut(environment,"Loading command:" + command ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)                
                continue

    def shutdownCommands(self, environment, section):
        for command in sorted(environment['commands'][section]):
            try:
                environment['commands'][section][command].shutdown(environment)
                environment['commands'][section][command] = None
            except Exception as e:
                print(e)
                environment['runtime']['debug'].writeDebugOut(environment,"Shutdown command:" + section + "." + cmd ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
                continue

    def executeTriggerCommands(self, environment, trigger):
        if environment['runtime']['screenManager'].isSuspendingScreen(environment):
            return
        for command in sorted(environment['commands'][trigger]):
            if self.commandExists(environment, command, trigger):        
                try:
                   environment['commands'][trigger][command].run(environment)
                except Exception as e:
                    print(e)
                    environment['runtime']['debug'].writeDebugOut(environment,"Executing trigger:" + trigger + "." + cmd ,debug.debugLevel.ERROR)
                    environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 

    def executeCommand(self, environment, command, section = 'commands'):
        if environment['runtime']['screenManager'].isSuspendingScreen(environment) :
            return    
        if self.commandExists(environment, command, section):
            try:
                if environment['generalInformation']['tutorialMode']:
                    description = environment['commands'][section][command].getDescription(environment)
                    environment['runtime']['outputManager'].presentText(environment, description, interrupt=True)                
                else:    
                    environment['commands'][section][command].run(environment)
            except Exception as e:
                print(e)
                
                environment['runtime']['debug'].writeDebugOut(environment,"Executing command:" + section + "." + command ,debug.debugLevel.ERROR)
                environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR) 
        self.clearCommandQueued(environment)
        environment['commandInfo']['lastCommandExecutionTime'] = time.time()    

    def isCommandQueued(self, environment):
        return environment['commandInfo']['currCommand'] != ''

    def clearCommandQueued(self, environment):
        environment['commandInfo']['currCommand'] = ''
        
    def queueCommand(self, environment, command):
        environment['commandInfo']['currCommand'] = command
        
    def commandExists(self, environment, command, section = 'commands'):
        return( command.upper() in environment['commands'][section]) 

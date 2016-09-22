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
        self.env = environment
        self.env['runtime']['commandManager'].loadCommands('commands')
        self.env['runtime']['commandManager'].loadCommands('onInput')
        self.env['runtime']['commandManager'].loadCommands('onScreenUpdate')         
        self.env['runtime']['commandManager'].loadCommands('onScreenChanged')
        self.env['runtime']['commandManager'].loadCommands('onApplicationChange')
        self.env['runtime']['commandManager'].loadCommands('onSwitchApplicationProfile')        

    def shutdown(self):
        self.env['runtime']['commandManager'].shutdownCommands('commands')
        self.env['runtime']['commandManager'].shutdownCommands('onInput')
        self.env['runtime']['commandManager'].shutdownCommands('onScreenUpdate')         
        self.env['runtime']['commandManager'].shutdownCommands('onScreenChanged')    
        self.env['runtime']['commandManager'].shutdownCommands('onApplicationChange') 
        self.env['runtime']['commandManager'].shutdownCommands('onSwitchApplicationProfile') 
        
    def loadCommands(self, section='commands'):
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
                    self.env['commands'][section][fileName.upper()] = command_mod.command()
                    self.env['commands'][section][fileName.upper()].initialize(self.env)
            except Exception as e:
                print(e)
                self.env['runtime']['debug'].writeDebugOut("Loading command:" + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                
                continue

    def shutdownCommands(self, section):
        for command in sorted(self.env['commands'][section]):
            try:
                self.env['commands'][section][command].shutdown()
                del self.env['commands'][section][command]
            except Exception as e:
                print(e)
                self.env['runtime']['debug'].writeDebugOut("Shutdown command:" + section + "." + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
                continue

    def executeSwitchTrigger(self, trigger, unLoadScript, loadScript):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return
        #unload
        oldScript = ''
        if isinstance(unLoadScript, list):
            if len(unLoadScript) == 0:
                oldScript = 'DEFAULT'
            else:
                oldScript = unLoadScript[0]
        elif unLoadScript:
            oldScript = str(unLoadScript)
        if oldScript == '':
            oldScript == 'DEFAULT'        
        if self.commandExists(oldScript, trigger):        
            try:
               self.env['commands'][trigger][oldScript].unload()         
            except Exception as e:
                print(e)
                self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + oldScript ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
        #load
        newScript = ''
        if isinstance(loadScript, list):
            if len(loadScript) == 0:
                newScript = 'DEFAULT'
            else:
                newScript = loadScript[0]
        elif unLoadScript:
            newScript = str(loadScript)
        if newScript == '':
            newScript == 'DEFAULT'
        if self.commandExists(newScript, trigger):        
            try:
               self.env['commands'][trigger][newScript].load()                      
            except Exception as e:
                print(e)
                self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + newScript ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                 

    def executeDefaultTrigger(self, trigger):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return
        for command in sorted(self.env['commands'][trigger]):
            if self.commandExists(command, trigger):        
                try:
                   self.env['commands'][trigger][command].run()
                except Exception as e:
                    print(e)
                    self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + command ,debug.debugLevel.ERROR)
                    self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 

    def executeCommand(self, command, section = 'commands'):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return    
        if self.commandExists(command, section):
            try:
                if self.env['generalInformation']['tutorialMode']:
                    description = self.env['commands'][section][command].getDescription()
                    self.env['runtime']['outputManager'].presentText(description, interrupt=True)                
                else:    
                    self.env['commands'][section][command].run()
            except Exception as e:
                print(e)
                
                self.env['runtime']['debug'].writeDebugOut("Executing command:" + section + "." + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
        self.clearCommandQueued()
        self.env['commandInfo']['lastCommandExecutionTime'] = time.time()    

    def isCommandQueued(self):
        return self.env['commandInfo']['currCommand'] != ''

    def clearCommandQueued(self):
        self.env['commandInfo']['currCommand'] = ''
        
    def queueCommand(self, command):
        self.env['commandInfo']['currCommand'] = command
        
    def commandExists(self, command, section = 'commands'):
        return( command.upper() in self.env['commands'][section]) 

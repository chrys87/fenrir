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
                    self.env['runtime']['debug'].writeDebugOut("Load command:" + section + "." + fileName.upper() ,debug.debugLevel.INFO)                    
                    
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Loading command:" + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                
                continue

    def shutdownCommands(self, section):
        for command in sorted(self.env['commands'][section]):
            try:
                self.env['commands'][section][command].shutdown()
                del self.env['commands'][section][command]
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Shutdown command:" + section + "." + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
                continue

    def executeSwitchTrigger(self, trigger, unLoadScript, loadScript):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return
        #unload
        oldScript = unLoadScript
        if self.commandExists(oldScript, trigger):        
            try:
               self.env['runtime']['debug'].writeDebugOut("Executing switchtrigger.unload:" + trigger + "." + oldScript ,debug.debugLevel.INFO)                 
               self.env['commands'][trigger][oldScript].unload()                     
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + oldScript ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
        #load
        newScript = loadScript
        if self.commandExists(newScript, trigger):        
            try:
               self.env['runtime']['debug'].writeDebugOut("Executing switchtrigger.load:" + trigger + "." + newScript ,debug.debugLevel.INFO)                    
               self.env['commands'][trigger][newScript].load()                                 
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + newScript ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                 

    def executeDefaultTrigger(self, trigger):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return
        for command in sorted(self.env['commands'][trigger]):
            if self.commandExists(command, trigger):        
                try:
                   self.env['runtime']['debug'].writeDebugOut("Executing trigger.command:" + trigger + "." + command ,debug.debugLevel.INFO)                    
                   self.env['commands'][trigger][command].run()                    
                except Exception as e:
                    self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + command ,debug.debugLevel.ERROR)
                    self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 

    def executeCommand(self, command, section = 'commands'):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return    
        if self.commandExists(command, section):
            try:
                if self.env['generalInformation']['tutorialMode']:
                    self.env['runtime']['debug'].writeDebugOut("Tutorial for command:" + section + "." + command ,debug.debugLevel.INFO)                   
                    description = self.env['commands'][section][command].getDescription()
                    self.env['runtime']['outputManager'].presentText(description, interrupt=True)                                       
                else:
                    self.env['runtime']['debug'].writeDebugOut("Executing command:" + section + "." + command ,debug.debugLevel.INFO)                    
                    self.env['commands'][section][command].run()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Executing command:" + section + "." + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR) 
        self.clearCommandQueued()
        self.env['commandInfo']['lastCommandExecutionTime'] = time.time()    

    def isCommandQueued(self):
        return self.env['commandInfo']['currCommand'] != ''

    def clearCommandQueued(self):
        self.env['commandInfo']['currCommand'] = ''
        
    def queueCommand(self, command):
        if command == '':
            return
        self.env['commandInfo']['currCommand'] = command
        
    def commandExists(self, command, section = 'commands'):
        return( command in self.env['commands'][section]) 

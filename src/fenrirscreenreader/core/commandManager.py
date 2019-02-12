#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import glob, os, time, inspect
currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import module_utils

class commandManager():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
        # commands
        self.env['commands'] = {}
        self.env['commandsIgnore'] = {}  
        for commandFolder in self.env['general']['commandFolderList']:
            self.env['runtime']['commandManager'].loadCommands(commandFolder)        
            if self.env['runtime']['settingsManager'].getSetting('general', 'commandPath') != '':
                self.env['runtime']['commandManager'].loadCommands(commandFolder,
                  self.env['runtime']['settingsManager'].getSetting('general', 'commandPath'))        

        # scripts for scriptKey
        self.env['runtime']['commandManager'].loadScriptCommands()
    
    def shutdown(self):
        for commandFolder in self.env['general']['commandFolderList']:    
            self.env['runtime']['commandManager'].shutdownCommands(commandFolder)

    def loadFile(self, filepath = ''):
        if filepath == '':
            return None
        if not os.path.exists(filepath):
            self.env['runtime']['debug'].writeDebugOut("loadFile: filepath not exists:" + filepath ,debug.debugLevel.WARNING)
            print('1')
            return None
        if os.path.isdir(filepath):
            print('2')
            self.env['runtime']['debug'].writeDebugOut("loadFile: filepath is a directory:" + filepath ,debug.debugLevel.ERROR)
            return None
        if not os.access(filepath, os.R_OK):
            print('3')
            self.env['runtime']['debug'].writeDebugOut("loadFile: filepath not readable:" + filepath ,debug.debugLevel.ERROR)
            return None

        try:
            fileName, fileExtension = os.path.splitext(filepath)
            fileName = fileName.split('/')[-1]
            if fileName.startswith('__'):
                return None
            if fileExtension.lower() == '.py':
                command_mod = module_utils.importModule(fileName, filepath)
                command = command_mod.command()
                command.initialize(self.env)
                self.env['runtime']['debug'].writeDebugOut("loadFile: Load command:" + filepath ,debug.debugLevel.INFO, onAnyLevel=True)
                return command
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut("loadFile: Loading command:" + filepath ,debug.debugLevel.ERROR)
            self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                
        return None
    def loadCommands(self, section='commands',commandPath=''):
        if commandPath =='':
            commandPath = fenrirPath+ "/commands/"
        if not commandPath.endswith('/'):
            commandPath += '/'
        commandFolder = commandPath + section +"/"
        if not os.path.exists(commandFolder):
            self.env['runtime']['debug'].writeDebugOut("loadCommands: commandFolder not exists:" + commandFolder ,debug.debugLevel.WARNING)                   
            return   
        if not os.path.isdir(commandFolder):
            self.env['runtime']['debug'].writeDebugOut("loadCommands: commandFolder not a directory:" + commandFolder ,debug.debugLevel.ERROR)                                    
            return
        if not os.access(commandFolder, os.R_OK):
            self.env['runtime']['debug'].writeDebugOut("loadCommands: commandFolder not readable:" + commandFolder ,debug.debugLevel.ERROR)                                    
            return
        self.env['commands'][section] = {}
        self.env['commandsIgnore'][section] = {}
        commandList = glob.glob(commandFolder+'*')
        for command in commandList:
            try:
                fileName, fileExtension = os.path.splitext(command)
                fileName = fileName.split('/')[-1]
                if fileName.startswith('__'):
                    continue
                try:
                    if self.env['commands'][section][fileName.upper()] != None:
                        continue
                except:
                    pass
                if fileExtension.lower() == '.py':
                    command_mod = module_utils.importModule(fileName, command)
                    self.env['commands'][section][fileName.upper()] = command_mod.command()
                    self.env['commandsIgnore'][section][fileName.upper()[fileName.upper().find('-')+1:]+'_IGNORE'] = False
                    self.env['commands'][section][fileName.upper()].initialize(self.env)
                    self.env['runtime']['debug'].writeDebugOut("loadCommands: Load command:" + section + "." + fileName.upper() ,debug.debugLevel.INFO, onAnyLevel=True)                    
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("loadCommands: Loading command:" + command ,debug.debugLevel.ERROR)
                self.env['runtime']['debug'].writeDebugOut(str(e),debug.debugLevel.ERROR)                
                continue
    
    def loadScriptCommands(self, section='commands', scriptPath=''):
        if scriptPath =='':
            scriptPath = self.env['runtime']['settingsManager'].getSetting('general', 'scriptPath')
        if not scriptPath.endswith('/'):
            scriptPath += '/'
        if not os.path.exists(scriptPath):
            if os.path.exists(fenrirPath +'/../../config/scripts/'):
                scriptPath = fenrirPath +'/../../config/scripts/'            
            else:
                self.env['runtime']['debug'].writeDebugOut("scriptpath not exists:" + scriptPath ,debug.debugLevel.WARNING)                            
                return   
        if not os.path.isdir(scriptPath):
            self.env['runtime']['debug'].writeDebugOut("scriptpath not a directory:" + scriptPath ,debug.debugLevel.ERROR)                                    
            return      
        if not os.access(scriptPath, os.R_OK):
            self.env['runtime']['debug'].writeDebugOut("scriptpath not readable:" + scriptPath ,debug.debugLevel.ERROR)                                    
            return         
        commandList = glob.glob(scriptPath+'*')
        subCommand = fenrirPath + '/commands/commands/subprocess.py'
        for command in commandList:
            invalid = False
            try:
                fileName, fileExtension = os.path.splitext(command)
                fileName = fileName.split('/')[-1]
                if fileName.startswith('__'):
                    continue
                if fileName.upper() in self.env['commands'][section]:
                    continue
                command_mod = module_utils.importModule(fileName ,subCommand)              
                self.env['commands'][section][fileName.upper()] = command_mod.command()
                self.env['commands'][section][fileName.upper()].initialize(self.env,command)
                self.env['runtime']['debug'].writeDebugOut("Load script:" + section + "." + fileName.upper() ,debug.debugLevel.INFO, onAnyLevel=True)                    
                commSettings = fileName.upper().split('__-__')
                if len(commSettings) == 1:
                    keys = commSettings[0]
                elif len(commSettings) == 2:
                    keys = commSettings[1]
                elif len(commSettings) > 2:
                    continue
                keys = keys.split('__+__')
                shortcutKeys = []
                shortcut = []
                for key in keys:
                    if not self.env['runtime']['inputManager'].isValidKey(key.upper()):
                        self.env['runtime']['debug'].writeDebugOut("invalid key : "+ key.upper() + ' script:' + fileName ,debug.debugLevel.WARNING)                    
                        invalid = True
                        break                
                    shortcutKeys.append(key.upper())
                if invalid:
                    continue                    
                if not 'KEY_SCRIPT' in shortcutKeys:
                    shortcutKeys.append('KEY_SCRIPT')                
                shortcut.append(1)
                shortcut.append(sorted(shortcutKeys)) 
                self.env['bindings'][str(shortcut)] = fileName.upper()                     
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Loading script:" + fileName ,debug.debugLevel.ERROR)
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

    def executeDefaultTrigger(self, trigger, force=False):
        if not force:
            if self.env['runtime']['screenManager'].isSuspendingScreen():
                return
        for command in sorted(self.env['commands'][trigger]):
            if self.commandExists(command, trigger):        
                try:
                    if self.env['commandsIgnore'][trigger][command[command.find('-')+1:]+'_IGNORE']:
                        self.env['commandsIgnore'][trigger][command[command.find('-')+1:]+'_IGNORE'] = False
                        self.env['runtime']['debug'].writeDebugOut("Ignore trigger.command:" + trigger + "." + command ,debug.debugLevel.INFO)                                
                    else:
                        self.env['runtime']['debug'].writeDebugOut("Executing trigger.command:" + trigger + "." + command ,debug.debugLevel.INFO)                    
                        self.env['commands'][trigger][command].run()                    
                except Exception as e:
                    self.env['runtime']['debug'].writeDebugOut("Executing trigger:" + trigger + "." + command + str(e) ,debug.debugLevel.ERROR)

    def executeCommand(self, command, section = 'commands'):
        if self.env['runtime']['screenManager'].isSuspendingScreen():
            return    
        if self.commandExists(command, section):
            try:
                if self.env['runtime']['helpManager'].isTutorialMode() and section != 'help':
                    self.env['runtime']['debug'].writeDebugOut("Tutorial for command:" + section + "." + command ,debug.debugLevel.INFO)                   
                    description = self.getCommandDescription(command, section)
                    self.env['runtime']['outputManager'].presentText(description, interrupt=True)                                       
                else:
                    self.env['runtime']['debug'].writeDebugOut("Executing command:" + section + "." + command ,debug.debugLevel.INFO)                    
                    self.runCommand(command, section)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Executing command:" + section + "." + command +' ' + str(e),debug.debugLevel.ERROR)

   
    def runCommand(self, command, section = 'commands'):
        if self.commandExists(command, section):
            try:
                self.env['runtime']['debug'].writeDebugOut("runCommand command:" + section + "." + command ,debug.debugLevel.INFO)                    
                self.env['commands'][section][command].run()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("runCommand command:" + section + "." + command +' ' + str(e),debug.debugLevel.ERROR)
        self.env['commandInfo']['lastCommandExecutionTime'] = time.time()    
        
    def getCommandDescription(self, command, section = 'commands'):
        if self.commandExists(command, section):
            try:
                return self.env['commands'][section][command].getDescription()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('commandManager.getCommandDescription:' + str(e),debug.debugLevel.ERROR) 
        self.env['commandInfo']['lastCommandExecutionTime'] = time.time()  
        
    def commandExists(self, command, section = 'commands'):
        try:
            return( command in self.env['commands'][section])
        except:
            return False
    def getShortcutForCommand(self, command):
        shortcut = ''
        try:
            shortcut = list(self.env['bindings'].keys())[list(self.env['bindings'].values()).index(command)]      
        except:
            pass
        return shortcut      

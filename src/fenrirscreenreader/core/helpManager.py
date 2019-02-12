#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug


class helpManager():
    def __init__(self):
        self.helpDict = {}
        self.tutorialListIndex = None
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass      
    def toggleTutorialMode(self):
        self.setTutorialMode(not self.env['general']['tutorialMode'])
    def setTutorialMode(self, newTutorialMode):
        if self.env['runtime']['vmenuManager'].getActive():
            return
        self.env['general']['tutorialMode'] = newTutorialMode
        if newTutorialMode:
            self.createHelpDict()
            self.env['bindings'][str([1, ['KEY_ESC']])] = 'TOGGLE_TUTORIAL_MODE'
            self.env['bindings'][str([1, ['KEY_UP']])] = 'PREV_HELP'
            self.env['bindings'][str([1, ['KEY_DOWN']])] = 'NEXT_HELP'
            self.env['bindings'][str([1, ['KEY_SPACE']])] = 'CURR_HELP'
        else:
            try:
                self.env['bindings'] = self.env['runtime']['settingsManager'].getBindingBackup()
            except:
                pass
    def isTutorialMode(self):
        return self.env['general']['tutorialMode']
    def getCommandHelpText(self, command, section = 'commands'):
        commandName = command.lower()
        commandName = commandName.split('__-__')[0]
        commandName = commandName.replace('_',' ')
        commandName = commandName.replace('_',' ')
        if command == 'TOGGLE_TUTORIAL_MODE':
            commandDescription = _('toggles the tutorial mode')
        else:
            commandDescription = self.env['runtime']['commandManager'].getCommandDescription( command, section = 'commands')
        if commandDescription == '':
            commandDescription = 'no Description available'
        commandShortcut = self.env['runtime']['commandManager'].getShortcutForCommand( command)
        commandShortcut = commandShortcut.replace('KEY_',' ')
        commandShortcut = commandShortcut.replace('[','')
        commandShortcut = commandShortcut.replace(']','')
        commandShortcut = commandShortcut.replace("'",'')
        if commandShortcut == '':
            commandShortcut = 'unbound'
        helptext = commandName + ', Shortcut ' + commandShortcut + ', Description ' + commandDescription
        return helptext
    def createHelpDict(self, section = 'commands'):
        self.helpDict = {}
        for command in sorted(self.env['commands'][section].keys()):
            self.helpDict[len(self.helpDict)] = self.getCommandHelpText(command, section)
        if len(self.helpDict) > 0:
            self.tutorialListIndex = 0
        else:
            self.tutorialListIndex = None
    def getHelpForCurrentIndex(self):
        if self.tutorialListIndex == None:
            return '' 
        return self.helpDict[self.tutorialListIndex]
    def nextIndex(self):
        if self.tutorialListIndex == None:
            return    
        self.tutorialListIndex += 1
        if self.tutorialListIndex >= len(self.helpDict):
           self.tutorialListIndex = 0 
    def prevIndex(self):
        if self.tutorialListIndex == None:
            return    
        self.tutorialListIndex -= 1
        if self.tutorialListIndex < 0:
           self.tutorialListIndex = len(self.helpDict) - 1                                                

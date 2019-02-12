#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import module_utils
import os, inspect, time

currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

class vmenuManager():
    def __init__(self):
        self.menuDict = {}
        self.currIndex = None
        self.currMenu = ''
        self.active = False
        self.reset = True
        self.useTimeout = True
        self.searchText = ''
        self.lastSearchTime = time.time()
    def initialize(self, environment):
        self.env = environment
        # use default path
        self.defaultVMenuPath = fenrirPath+ "/commands/vmenu-profiles/" + self.env['runtime']['inputManager'].getShortcutType()
        # if there is no user configuration
        if self.env['runtime']['settingsManager'].getSetting('menu', 'vmenuPath') != '':
            self.defaultVMenuPath = self.env['runtime']['settingsManager'].getSetting('menu', 'vmenuPath')
            if not self.defaultVMenuPath.endswith('/'):
                self.defaultVMenuPath += '/'
            self.defaultVMenuPath += self.env['runtime']['inputManager'].getShortcutType()

        self.createMenuTree()
        self.closeAfterAction = False
    def shutdown(self):
        pass
    def clearSearchText(self):
        self.searchText = ''
    def searchEntry(self, value, forceReset = False):
        if self.currIndex == None:
            return ''
        if self.reset or forceReset:
            self.clearSearchText()
        else:
            if self.useTimeout:
                if time.time() - self.lastSearchTime > 1:
                    self.clearSearchText()
        self.searchText += value.upper()
        self.lastSearchTime = time.time()
        startIndex = self.getCurrIndex()
        while True:
            if not self.nextIndex():
                return ''
            entry = self.getCurrentEntry()
            if entry.upper().startswith(self.searchText):
                return entry
            if startIndex == self.getCurrIndex():
                return ''

    def setCurrMenu(self, currMenu = ''):
        self.currIndex = None
        self.currMenu = ''
        if currMenu != '':
            currMenu += ' ' + _('Menu')
            try:
                t = self.menuDict[currMenu]
                l = list(self.menuDict.keys())
                self.currIndex = [l.index(currMenu)]
            except Exception as e:
                print(e)
                self.currMenu = ''
                self.currIndex = None
                return
            if self.incLevel():
                self.currMenu = currMenu
            else:
                self.currMenu = ''
                self.currIndex = None
    def getCurrMenu(self):
        return self.currMenu
    def getActive(self):
        return self.active
    def togglelVMenuMode(self, closeAfterAction = True):
        self.setActive(not self.getActive(), closeAfterAction)
    def setActive(self, active, closeAfterAction = True):
        if self.env['runtime']['helpManager'].isTutorialMode():
            return
        self.active = active
        if self.active:
            self.closeAfterAction = closeAfterAction
            try:
                self.createMenuTree()
            except Exception as e:
                print(e)
            try:
                if self.currMenu != '':
                    self.setCurrMenu(self.currMenu)
                if self.currIndex == None:
                    if len(self.menuDict) > 0:
                        self.currIndex = [0]
            except Exception as e:
                print(e)
            try:
                # navigation
                self.env['bindings'][str([1, ['KEY_ESC']])] = 'TOGGLE_VMENU_MODE'
                self.env['bindings'][str([1, ['KEY_UP']])] = 'PREV_VMENU_ENTRY'
                self.env['bindings'][str([1, ['KEY_DOWN']])] = 'NEXT_VMENU_ENTRY'
                self.env['bindings'][str([1, ['KEY_SPACE']])] = 'CURR_VMENU_ENTRY'
                self.env['bindings'][str([1, ['KEY_LEFT']])] = 'DEC_LEVEL_VMENU'
                self.env['bindings'][str([1, ['KEY_RIGHT']])] = 'INC_LEVEL_VMENU'
                self.env['bindings'][str([1, ['KEY_ENTER']])] = 'EXEC_VMENU_ENTRY'
                # search
                self.env['bindings'][str([1, ['KEY_A']])] = 'SEARCH_A'
                self.env['bindings'][str([1, ['KEY_B']])] = 'SEARCH_B'
                self.env['bindings'][str([1, ['KEY_C']])] = 'SEARCH_C'
                self.env['bindings'][str([1, ['KEY_D']])] = 'SEARCH_D'
                self.env['bindings'][str([1, ['KEY_E']])] = 'SEARCH_E'
                self.env['bindings'][str([1, ['KEY_F']])] = 'SEARCH_F'
                self.env['bindings'][str([1, ['KEY_G']])] = 'SEARCH_G'
                self.env['bindings'][str([1, ['KEY_H']])] = 'SEARCH_H'
                self.env['bindings'][str([1, ['KEY_I']])] = 'SEARCH_I'
                self.env['bindings'][str([1, ['KEY_J']])] = 'SEARCH_J'
                self.env['bindings'][str([1, ['KEY_K']])] = 'SEARCH_K'
                self.env['bindings'][str([1, ['KEY_L']])] = 'SEARCH_L'
                self.env['bindings'][str([1, ['KEY_M']])] = 'SEARCH_M'
                self.env['bindings'][str([1, ['KEY_N']])] = 'SEARCH_N'
                self.env['bindings'][str([1, ['KEY_O']])] = 'SEARCH_O'
                self.env['bindings'][str([1, ['KEY_P']])] = 'SEARCH_P'
                self.env['bindings'][str([1, ['KEY_Q']])] = 'SEARCH_Q'
                self.env['bindings'][str([1, ['KEY_R']])] = 'SEARCH_R'
                self.env['bindings'][str([1, ['KEY_S']])] = 'SEARCH_S'
                self.env['bindings'][str([1, ['KEY_T']])] = 'SEARCH_T'
                self.env['bindings'][str([1, ['KEY_U']])] = 'SEARCH_U'
                self.env['bindings'][str([1, ['KEY_V']])] = 'SEARCH_V'
                self.env['bindings'][str([1, ['KEY_W']])] = 'SEARCH_W'
                self.env['bindings'][str([1, ['KEY_X']])] = 'SEARCH_X'
                self.env['bindings'][str([1, ['KEY_Y']])] = 'SEARCH_Y'
                self.env['bindings'][str([1, ['KEY_Z']])] = 'SEARCH_Z'
            except Exception as e:
                print(e)
        else:
            try:
                self.currIndex = None
                self.env['bindings'] = self.env['runtime']['settingsManager'].getBindingBackup()
            except:
                pass
    def createMenuTree(self):
        self.currIndex = None
        menu = self.fs_tree_to_dict( self.defaultVMenuPath)
        if menu:
            self.menuDict = menu
    def executeMenu(self):
        if self.currIndex == None:
            return
        try:
            command = self.getValueByPath(self.menuDict, self.currIndex)
            if not command == None:
                command.run()
                if self.closeAfterAction:
                    self.setActive(False)
        except Exception as e:
            try:
                self.incLevel()
                text = self.getCurrentEntry()
                self.env['runtime']['outputManager'].presentText(text, interrupt=True)                
            except:
                print(e)

    def incLevel(self):
        if self.currIndex == None:
            return False
        try:
            r = self.getValueByPath(self.menuDict, self.currIndex +[0])
            if r == {}:
                return False
        except:
            return False
        self.currIndex.append(0)
        return True
    def decLevel(self):
        if self.currIndex == None:
            return False
        if self.currMenu != '':
            if len(self.currIndex) <= 2:
                return False
        elif len(self.currIndex) == 1:
            return False
        self.currIndex = self.currIndex[:len(self.currIndex) - 1]
        return True
    def nextIndex(self):
        if self.currIndex == None:
            return False
        if self.currIndex[len(self.currIndex) - 1] + 1 >= len(self.getNestedByPath(self.menuDict, self.currIndex[:-1])):
           self.currIndex[len(self.currIndex) - 1] = 0 
        else:
            self.currIndex[len(self.currIndex) - 1] += 1
        return True
    def getCurrIndex(self):
        if self.currIndex == None:
            return 0        
        return self.currIndex[len(self.currIndex) - 1]
    def prevIndex(self):
        if self.currIndex == None:
            return False
        if self.currIndex[len(self.currIndex) - 1] == 0:
           self.currIndex[len(self.currIndex) - 1] = len(self.getNestedByPath(self.menuDict, self.currIndex[:-1])) - 1
        else:
            self.currIndex[len(self.currIndex) - 1] -= 1
        return True

    def getCurrentEntry(self):
        return self.getKeysByPath(self.menuDict, self.currIndex)[self.currIndex[-1]]
    def fs_tree_to_dict(self, path_):
        for root, dirs, files in os.walk(path_):
            tree = {d + ' ' + _('Menu'): self.fs_tree_to_dict(os.path.join(root, d)) for d in dirs if not d.startswith('__')}
            for f in files:
                try:
                    fileName, fileExtension = os.path.splitext(f)
                    fileName = fileName.split('/')[-1]
                    if fileName.startswith('__'):
                        continue
                    command = self.env['runtime']['commandManager'].loadFile(root + '/' + f)
                    tree.update({fileName + ' ' + _('Action'): command})
                except Exception as e:
                    print(e)
            return tree  # note we discontinue iteration trough os.walk
    def getNestedByPath(self, complete, path):
        path = path.copy()
        if path != []:
            index = list(complete.keys())[path[0]]
            nested = self.getNestedByPath(complete[index], path[1:])
            return nested
        else:
            return complete


    def getKeysByPath(self, complete, path):
        if not isinstance(complete, dict):
            return[]
        d = complete
        for i in path[:-1]:
            d = d[list(d.keys())[i]]
        return list(d.keys())

    def getValueByPath(self, complete, path):
        if not isinstance(complete, dict):
            return complete
        d = complete.copy()
        for i in path:
            d = d[list(d.keys())[i]]
        return d

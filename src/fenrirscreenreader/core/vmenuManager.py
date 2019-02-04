#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import module_utils
import os, inspect

currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

class vmenuManager():
    def __init__(self):
        self.menuDict = {}
        self.currIndex = None
        self.currMenu = ''
        self.active = False
    def initialize(self, environment):
        self.env = environment
        self.defaultVMenuPath = fenrirPath+ "/commands/vmenu-profiles/" + self.env['runtime']['inputManager'].getShortcutType()
    def shutdown(self):
        pass
    def setCurrMenu(self, currMenu = ''):
        try:
            t = self.menuDict[currMenu]
            l = list(menuDict.keys())
            self.currIndex = [l.index(currMenu)]
            self.currMenu = currMenu
        except:
            self.currIndex = None
            self.currMenu = ''
    def getCurrMenu(self):
        return self.currMenu
    def getActive(self):
        return self.active
    def togglelVMenuMode(self):
        self.setActive(not self.getActive())
    def setActive(self, active):
        self.active = active
        if self.active:
            #try:
            self.createMenuTree()
            #except Exception as e:
            #    print(e)
            try:
                self.env['bindings'][str([1, ['KEY_ESC']])] = 'TOGGLE_VMENU_MODE'
                self.env['bindings'][str([1, ['KEY_UP']])] = 'PREV_VMENU_ENTRY'
                self.env['bindings'][str([1, ['KEY_DOWN']])] = 'NEXT_VMENU_ENTRY'
                self.env['bindings'][str([1, ['KEY_SPACE']])] = 'CURR_VMENU_ENTRY'
                self.env['bindings'][str([1, ['KEY_LEFT']])] = 'DEC_LEVEL_VMENU'
                self.env['bindings'][str([1, ['KEY_RIGHT']])] = 'INC_LEVEL_VMENU'
                self.env['bindings'][str([1, ['KEY_ENTER']])] = 'EXEC_VMENU_ENTRY'
            except Exception as e:
                print(e)
        else:
            try:
                self.menuDict = {}
                self.currIndex = None
                self.currMenu = ''
                del(self.env['bindings'][str([1, ['KEY_ESC']])])
                del(self.env['bindings'][str([1, ['KEY_UP']])])
                del(self.env['bindings'][str([1, ['KEY_DOWN']])])
                del(self.env['bindings'][str([1, ['KEY_SPACE']])])
                del(self.env['bindings'][str([1, ['KEY_LEFT']])])
                del(self.env['bindings'][str([1, ['KEY_RIGHT']])])
                del(self.env['bindings'][str([1, ['KEY_ENTER']])])
            except:
                pass
    def createMenuTree(self):
        self.currIndex = None
        menu = self.fs_tree_to_dict( self.defaultVMenuPath)
        if menu:
            self.menuDict = menu
            if len(self.menuDict) > 0:
                self.currIndex = [0]
    def executeMenu(self):
        if self.currIndex == None:
            return
        try:
            command = self.getValueByPath(self.menuDict, self.currIndex)
            if not command == None:
                command.run()
        except Exception as e:
            print(e)
            self.incLevel()
    def incLevel(self):
        if self.currIndex == None:
            return
        try:
            r = self.getValueByPath(self.menuDict, self.currIndex +[0])
            print(r)
            #if not r:
            #    return
            if r == {}:
                return
        except:
            return
        self.currIndex.append(0)
        print(self.currIndex)
    def decLevel(self):
        if self.currIndex == None:
            return
        if len(self.currIndex) == 1:
            return
        self.currIndex.remove(len(self.currIndex) - 1)
        print(self.currIndex)
    def nextIndex(self):
        if self.currIndex == None:
            return
        if self.currIndex[len(self.currIndex) - 1] + 1 >= len(self.getNestedByPath(self.menuDict, self.currIndex[:-1])):
           self.currIndex[len(self.currIndex) - 1] = 0 
        else:
            self.currIndex[len(self.currIndex) - 1] += 1
        print(self.currIndex)

    def prevIndex(self):
        if self.currIndex == None:
            return
        if self.currIndex[len(self.currIndex) - 1] == 0:
           self.currIndex[len(self.currIndex) - 1] = len(self.getNestedByPath(self.menuDict, self.currIndex[:-1])) - 1
        else:
            self.currIndex[len(self.currIndex) - 1] -= 1
        print(self.currIndex)

    def getCurrentEntry(self):
        print( self.getKeysByPath(self.menuDict, self.currIndex)[self.currIndex[-1]])
        return self.getKeysByPath(self.menuDict, self.currIndex)[self.currIndex[-1]]
    def fs_tree_to_dict(self, path_):
        for root, dirs, files in os.walk(path_):
            tree = {d: self.fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
            for f in files:
                try:
                    command = self.env['runtime']['commandManager'].loadFile(root + '/' + f)
                    tree.update({f: command})
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
            return None
        d = complete.copy()
        for i in path:
            d = d[list(d.keys())[i]]
        return d
'''
import os
level = [0]

def fs_tree_to_dict( path_):
    file_token = ''
    for root, dirs, files in os.walk(path_):
        tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
        print(files, root, dirs)
        tree.update({f: root + '/' + f for f in files})
        return tree  # note we discontinue iteration trough os.walk


v = fs_tree_to_dict( '/home/chrys/Projekte/fenrir/src/fenrirscreenreader/commands/vmenu/KEY')        


def getNestedByPath(complete, path):
    path = path.copy()
    if path != []:
        index = list(complete.keys())[path[0]]
        path.remove(0)
        nested = getNestedByPath(complete[index], path)
        return nested
    else:
        return complete

def getKeysByPath(complete, path):
    d = complete
    for i in path[:-1]:
        d = d[list(d.keys())[i]]
    return list(d.keys())


def getValueByPath(complete, path):
    d = complete
    for i in path:
        d = d[list(d.keys())[i]]
    return d


c = [0,0,0]


getKeysByPath(v,c)
getValueByPath(v,c)

'''

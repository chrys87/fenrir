#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import os


class vmenuManager():
    def __init__(self):
        self.menuDict = {}
        self.currMenu = {}
        self.currIndex = None
        self.currLevel = None
        self.active = False
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getActive(self):
        return self.active
    def togglelMode(self):
        self.setActive(not self.getActive())
    def setActive(self, active):
        self.active = active
        if active:
            self.createHelpDict()        
            self.env['bindings'][str([1, ['KEY_ESC']])] = 'TOGGLE_TUTORIAL_MODE'
            self.env['bindings'][str([1, ['KEY_UP']])] = 'PREV_HELP'
            self.env['bindings'][str([1, ['KEY_DOWN']])] = 'NEXT_HELP'
            self.env['bindings'][str([1, ['KEY_SPACE']])] = 'CURR_HELP'                                    
        else:
            try:
                del(self.env['bindings'][str([1, ['KEY_ESC']])])
                del(self.env['bindings'][str([1, ['KEY_UP']])])
                del(self.env['bindings'][str([1, ['KEY_DOWN']])])
                del(self.env['bindings'][str([1, ['KEY_SPACE']])])
            except:
                pass                     

    def createHelpDict(self, section = 'commands'):
        self.menuDict = {}        
        #for command in sorted(self.env['commands'][section].keys()):
        #    self.menuDict[len(self.menuDict)] = self.getCommandHelpText(command, section)            
        if len(self.menuDict) > 0:
            self.currIndex = 0
        else:
            self.currIndex = None        
    def getHelpForCurrentIndex(self):            
        if self.currIndex == None:
            return '' 
        return self.menuDict[self.currIndex]
    def nextIndex(self):
        if self.currIndex == None:
            return    
        self.currIndex += 1
        if self.currIndex >= len(self.menuDict):
           self.currIndex = 0 
    def prevIndex(self):
        if self.currIndex == None:
            return    
        self.currIndex -= 1
        if self.currIndex < 0:
           self.currIndex = len(self.menuDict) - 1
    def fs_tree_to_dict(self, path_):
        for root, dirs, files in os.walk(path_):
            tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
            tree.update({f: root + f for f in files})
            return tree  # note we discontinue iteration trough os.walk
''''
import os
level = [0]

def fs_tree_to_dict( path_):
    file_token = ''
    for root, dirs, files in os.walk(path_):
        tree = {d: fs_tree_to_dict(os.path.join(root, d)) for d in dirs}
        print(files, root, dirs)
        tree.update({f: root + f for f in files})
        return tree  # note we discontinue iteration trough os.walk

v = fs_tree_to_dict( '/home/chrys/Projekte/fenrir/src/fenrirscreenreader/commands/vmenu')        



''''

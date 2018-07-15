#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import line_utils
from fenrirscreenreader.utils import word_utils

class command():
    def __init__(self):
        self.lastIdent = -1
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return ''        
    
    def run(self):
        if not self.env['runtime']['settingsManager'].getSettingAsBool('focus', 'cursor'):
            return      
        if self.env['runtime']['screenManager'].isScreenChange():
            self.lastIdent = 0        
            return        
        # this leads to problems in vim -> status line change -> no announcement, so we do check the lengh as hack
        if self.env['runtime']['screenManager'].isDelta():
            return
            
        # is a vertical change?
        if not self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return   
       
        x, y, currLine = line_utils.getCurrentLine(self.env['screen']['newCursor']['x'], self.env['screen']['newCursor']['y'], self.env['screen']['newContentText'])
        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True, flush=False)
        else:
            # ident
            currIdent = len(currLine) - len(currLine.lstrip())
            if self.lastIdent == -1:
                self.lastIdent = currIdent
            doInterrupt = True                
            if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'autoPresentIndent'):
                if self.lastIdent != currIdent: 
                    self.env['runtime']['outputManager'].presentText(_('indented ') + str(currIdent) + ' ', interrupt=doInterrupt, flush=False)
                    doInterrupt = False    
            # barrier
            sayLine = currLine        
            if self.env['runtime']['settingsManager'].getSettingAsBool('barrier','enabled'):
                isBarrier, barrierLine = self.env['runtime']['barrierManager'].handleLineBarrier(self.env['screen']['newContentText'].split('\n'), self.env['screen']['newCursor']['x'],self.env['screen']['newCursor']['y'])
                if isBarrier:
                    sayLine = barrierLine
            # output
            self.env['runtime']['outputManager'].presentText(sayLine, interrupt=doInterrupt, flush=False)
            self.lastIdent = currIdent
    def setCallback(self, callback):
        pass


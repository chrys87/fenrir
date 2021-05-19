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

        # is a vertical change?
        if not self.env['runtime']['cursorManager'].isCursorHorizontalMove():
            return
        x, y, currLine = line_utils.getCurrentLine(self.env['screen']['newCursor']['x'], self.env['screen']['newCursor']['y'], self.env['screen']['newContentText'])
        currIdent = self.env['screen']['newCursor']['x']

        if not currLine.isspace():
            # ident
            lastIdent, lastY, lastLine = line_utils.getCurrentLine(self.env['screen']['newCursor']['x'], self.env['screen']['newCursor']['y'], self.env['screen']['oldContentText'])
            if currLine.strip() != lastLine.strip():
                return
            if len(currLine.lstrip()) == len(lastLine.lstrip()):
                return

            currIdent = len(currLine) - len(currLine.lstrip())

            if self.lastIdent == -1:
                self.lastIdent = currIdent
            if currIdent <= 0:
                return
        if self.env['runtime']['settingsManager'].getSettingAsBool('general', 'autoPresentIndent'):
            if self.env['runtime']['settingsManager'].getSettingAsInt('general', 'autoPresentIndentMode') in [0,1]:
                self.env['runtime']['outputManager'].playFrequence(currIdent * 50, 0.1, interrupt=False)
            if self.env['runtime']['settingsManager'].getSettingAsInt('general', 'autoPresentIndentMode') in [0,2]:
                if self.lastIdent != currIdent: 
                    self.env['runtime']['outputManager'].presentText(_('indented ') + str(currIdent) + ' ', interrupt=False, flush=False)
        self.lastIdent = currIdent
    def setCallback(self, callback):
        pass


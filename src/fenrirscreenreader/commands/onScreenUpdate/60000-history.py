#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return ''        
    def run(self):
        if self.env['screen']['newAttribDelta'] != '':
            return  
        if self.env['runtime']['screenManager'].isScreenChange():
            return
        if self.env['runtime']['cursorManager'].isCursorVerticalMove():
            return
        if self.env['runtime']['attributeManager'].isAttributeChange():
            return
        # hack for pdmenu and maybe other dialog apps that place the cursor at last cell/row
        # this is not to be identified as history
        if (self.env['screen']['newCursor']['x'] == self.env['runtime']['screenManager'].getColumns() - 1) and (self.env['screen']['newCursor']['y'] == self.env['runtime']['screenManager'].getRows() - 1):
            return
        if self.env['runtime']['inputManager'].getShortcutType() in ['KEY']:
            if not (self.env['runtime']['inputManager'].getLastDeepestInput() in [['KEY_UP'],['KEY_DOWN']]):
                return 
        if self.env['runtime']['inputManager'].getShortcutType() in ['BYTE']:
            if not (self.env['runtime']['byteManager'].getLastByteKey() in [b'^[[A',b'^[[B']):
                return 
                
        prevLine = self.env['screen']['oldContentText'].split('\n')[self.env['screen']['newCursor']['y']]
        currLine = self.env['screen']['newContentText'].split('\n')[self.env['screen']['newCursor']['y']]            
        if prevLine == currLine:
            if self.env['screen']['newDelta'] != '':
                return         
        if not currLine.isspace():
            currPrompt = currLine.find('$')
            rootPrompt = currLine.find('#')
            if currPrompt <= 0:
                if rootPrompt > 0:
                    currPrompt = rootPrompt
                else:
                    announce = currLine            
            if currPrompt > 0:
                remove_digits = str.maketrans('0123456789', '          ')
                if prevLine[:currPrompt].translate(remove_digits) == currLine[:currPrompt].translate(remove_digits):
                    announce = currLine[currPrompt+1:]
                else:
                    announce = currLine                      

        if currLine.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True, flush=False)
        else:            
            self.env['runtime']['outputManager'].presentText(announce, interrupt=True, flush=False)
        self.env['commandsIgnore']['onScreenUpdate']['CHAR_DELETE_ECHO'] = True
        self.env['commandsIgnore']['onScreenUpdate']['CHAR_ECHO'] = True
        self.env['commandsIgnore']['onScreenUpdate']['INCOMING_IGNORE'] = True
    def setCallback(self, callback):
        pass


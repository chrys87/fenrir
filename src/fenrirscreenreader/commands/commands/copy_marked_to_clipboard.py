#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import mark_utils

class command():
    def __init__(self):
        pass
        
    def initialize(self, environment):
        self.env = environment
        
    def shutdown(self):
        pass 
        
    def getDescription(self):
        return _('copies marked text to the currently selected clipboard')    
    
    def getTextFromScreen(self, startMark, endMark):
        screenContent = self.env['screen']['newContentText']
        screenLines = screenContent.split('\n')
        
        startY = min(startMark['y'], len(screenLines) - 1)
        endY = min(endMark['y'], len(screenLines) - 1)
        
        # If marks are on the same line
        if startY == endY:
            line = screenLines[startY]
            startX = min(startMark['x'], len(line))
            endX = min(endMark['x'], len(line)) + 1
            return line[startX:endX]
            
        # Handle multi-line selection
        result = []
        
        # First line (from start mark to end of line)
        firstLine = screenLines[startY]
        startX = min(startMark['x'], len(firstLine))
        result.append(firstLine[startX:])
        
        # Middle lines (complete lines)
        for lineNum in range(startY + 1, endY):
            result.append(screenLines[lineNum])
            
        # Last line (from start to end mark)
        if endY > startY:
            lastLine = screenLines[endY]
            endX = min(endMark['x'], len(lastLine)) + 1
            result.append(lastLine[:endX])
            
        return '\n'.join(result)
    
    def run(self):
        if not self.env['commandBuffer']['Marks']['1']:
            self.env['runtime']['outputManager'].presentText(_("One or two marks are needed"), interrupt=True)
            return
        if not self.env['commandBuffer']['Marks']['2']:
            self.env['runtime']['cursorManager'].setMark()
            
        # use the last first and the last setted mark as range
        startMark = self.env['commandBuffer']['Marks']['1'].copy()
        endMark = self.env['commandBuffer']['Marks']['2'].copy()         
        
        # Replace mark_utils.getTextBetweenMarks with our new method
        marked = self.getTextFromScreen(startMark, endMark)
        
        self.env['runtime']['memoryManager'].addValueToFirstIndex('clipboardHistory', marked)
        # reset marks
        self.env['runtime']['cursorManager'].clearMarks()      
        self.env['runtime']['outputManager'].presentText(marked, soundIcon='CopyToClipboard', interrupt=True)
        
    def setCallback(self, callback):
        pass

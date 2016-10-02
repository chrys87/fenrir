#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from utils import mark_utils
from utils import line_utils

class command():
    def __init__(self):
        self.ID = '2'
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return 'read Bookmark ' + self.ID

    def run(self):
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        if not self.env['commandBuffer']['bookMarks'][self.ID]:
            self.env['runtime']['outputManager'].presentText("Bookmark " + self.ID + "not set", interrupt=True)
            return
        if not self.env['commandBuffer']['bookMarks'][self.ID][currApp]:
            self.env['runtime']['outputManager'].presentText("Bookmark for application " + currApp + " not set", interrupt=True)
            return
        if not self.env['commandBuffer']['bookMarks'][self.ID][currApp]['1']:
            self.env['runtime']['outputManager'].presentText("Bookmark for application " + currApp + " not set", interrupt=True)
            return
        print('i',self.env['commandBuffer']['bookMarks'][self.ID][currApp]['1'])
        # set marks
        marked = ''
        startMark = self.env['commandBuffer']['bookMarks'][self.ID][currApp]['1'].copy()
        if self.env['commandBuffer']['bookMarks'][self.ID][currApp]['2']:
            endMark = self.env['commandBuffer']['bookMarks'][self.ID][currApp]['2'].copy()
            marked = mark_utils.getTextBetweenMarks(startMark, endMark, self.env['screenData']['newContentText'])
        else:
            x, y, marked = \
              line_utils.getCurrentLine(startMark['x'], startMark['y'], self.env['screenData']['newContentText'])
        if marked.strip(" \t\n") == '':
            self.env['runtime']['outputManager'].presentText("blank", soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(marked, interrupt=True)

    def setCallback(self, callback):
        pass

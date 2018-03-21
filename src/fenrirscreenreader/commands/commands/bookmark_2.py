#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import mark_utils
from fenrirscreenreader.utils import line_utils

class command():
    def __init__(self):
        self.ID = '2'
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass 
    def getDescription(self):
        return _('read Bookmark {0}').format(self.ID,)

    def run(self):
        currApp = self.env['runtime']['applicationManager'].getCurrentApplication()
        if not self.env['commandBuffer']['bookMarks'][self.ID]:
            self.env['runtime']['outputManager'].presentText(_('Bookmark {0} not set').format(self.ID,), interrupt=True)
            return
        if not self.env['commandBuffer']['bookMarks'][self.ID][currApp]:
            self.env['runtime']['outputManager'].presentText(_('Bookmark for application {0} not set').format(currApp,), interrupt=True)
            return
        if not self.env['commandBuffer']['bookMarks'][self.ID][currApp]['1']:
            self.env['runtime']['outputManager'].presentText(_('Bookmark for application {0} not set').format(currApp,), interrupt=True)
            return

        # set marks
        marked = ''
        startMark = self.env['commandBuffer']['bookMarks'][self.ID][currApp]['1'].copy()
        if self.env['commandBuffer']['bookMarks'][self.ID][currApp]['2']:
            endMark = self.env['commandBuffer']['bookMarks'][self.ID][currApp]['2'].copy()
            marked = mark_utils.getTextBetweenMarks(startMark, endMark, self.env['screen']['newContentText'])
        else:
            x, y, marked = \
              line_utils.getCurrentLine(startMark['x'], startMark['y'], self.env['screen']['newContentText'])
        if marked.isspace():
            self.env['runtime']['outputManager'].presentText(_("blank"), soundIcon='EmptyLine', interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(marked, interrupt=True)

    def setCallback(self, callback):
        pass

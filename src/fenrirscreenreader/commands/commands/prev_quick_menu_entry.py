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
        return _('get previous quick menu entry')
    def run(self):
        menu = ''
        value = ''
        if self.env['runtime']['quickMenuManager'].prevEntry():
            menu = self.env['runtime']['quickMenuManager'].getCurrentEntry()
            if menu != '':
                value = self.env['runtime']['quickMenuManager'].getCurrentValue()
                self.env['runtime']['outputManager'].presentText(menu + ' ' + value, interrupt=True)
        else:
            self.env['runtime']['outputManager'].presentText(_('Quick menu not available'), interrupt=True)
    def setCallback(self, callback):
        pass

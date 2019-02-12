#!/usr/bin/env python
# -*- encoding: utf-8
from fenrirscreenreader.core import debug


class command():
    def __init__(self):
        pass

    def initialize(self, environment):
        self.env = environment
        self.keyMakro = [[1, 'KEY_LEFTCTRL'],
                         [1, 'KEY_G'],
                         [0.05, 'SLEEP'],
                         [0, 'KEY_G'],
                         [0, 'KEY_LEFTCTRL']]

    def shutdown(self):
        pass

    def getDescription(self):
        return "Learn about the Nano text editor."

    def run(self):
        self.env['runtime']['outputManager'].presentText(
            "Okay, loading the information about Nano.", interrupt=True)
        if self.env['runtime']['inputManager'].getShortcutType() in ['KEY']:
            self.env['runtime']['inputManager'].sendKeys(self.keyMakro)
        elif self.env['runtime']['inputManager'].getShortcutType() in ['BYTE']:
            self.env['runtime']['byteManager'].sendBytes(self.byteMakro)

    def setCallback(self, callback):
        pass

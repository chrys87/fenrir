#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

initialized = False
try:
    import alsaaudio
    initialized = True
except:
    pass

from fenrirscreenreader.core import debug

class command():
    def __init__(self):
        pass
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return _("Decrease system volume")         

    def run(self):
        if not initialized:
           self.env['runtime']['outputManager'].presentText(_('alsaaudio is not installed'), interrupt=True) 
           return
        mixer = alsaaudio.Mixer()
        value = mixer.getvolume()[0]
        value = value - 5
        if value < 5:
            value = 5
        mixer.setvolume(value)
        self.env['runtime']['outputManager'].presentText(_("{0} percent system volume").format(value), interrupt=True)

    def setCallback(self, callback):
        pass

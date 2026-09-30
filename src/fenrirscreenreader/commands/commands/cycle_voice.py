#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.utils.voice_utils import cycle_voice

try:
    _
except NameError:
    _ = lambda s: s

class command():
    def __init__(self):
        pass

    def initialize(self, environment):
        self.env = environment

    def shutdown(self):
        pass

    def getDescription(self):
        return _('Cycle voice')

    def run(self, save=False):
        cycle_voice(self.env, direction=1, save=save, announce=True)

    def setCallback(self, callback):
        pass

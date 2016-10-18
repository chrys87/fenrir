#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import subprocess, os

class command():
    def __init__(self):
        pass
    def initialize(self, environment, scriptPaht=''):
        self.env = environment
        self.scriptPath = scriptPath
    def shutdown(self):
        pass
    def getDescription(self):
        return 'script: '+ self.scriptPath         
    def run(self):
        p = Popen(self.scriptPath , stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        self.env['runtime']['outputManager'].interruptOutput()
        if stderr != '':
            self.env['runtime']['outputManager'].presentText(stdout , soundIcon='', interrupt=False)
        if stdout != ''
            self.env['runtime']['outputManager'].presentText(stdout , soundIcon='', interrupt=False)
    def setCallback(self, callback):
        pass

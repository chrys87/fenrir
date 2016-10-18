#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import subprocess, os
from subprocess import Popen, PIPE

class command():
    def __init__(self):
        pass
    def initialize(self, environment, scriptPath=''):
        self.env = environment
        self.scriptPath = scriptPath
    def shutdown(self):
        pass
    def getDescription(self):
        return 'script: ' + os.path.basename(self.scriptPath) + ' fullpath: '+ self.scriptPath
    def run(self):
        if not os.path.exists(self.scriptPath):
            self.env['runtime']['outputManager'].presentText('scriptfile does not exist' , soundIcon='', interrupt=False)
            return   
        if not os.path.isfile(self.scriptPath):
            self.env['runtime']['outputManager'].presentText('scriptfile is not a file' , soundIcon='', interrupt=False)
            return      
        if not os.access(self.scriptPath, os.X_OK):
            self.env['runtime']['outputManager'].presentText('scriptfile is not executable' , soundIcon='', interrupt=False)
            return                            
        p = Popen(self.scriptPath , stdout=PIPE, stderr=PIPE, shell=True)
        stdout, stderr = p.communicate()
        self.env['runtime']['outputManager'].interruptOutput()
        stderr = str(stderr)
        stdout = str(stdout)
        if stderr != '':
            self.env['runtime']['outputManager'].presentText(stdout , soundIcon='', interrupt=False)
        if stdout != '':
            self.env['runtime']['outputManager'].presentText(stdout , soundIcon='', interrupt=False)
    def setCallback(self, callback):
        pass

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import subprocess, os
from subprocess import Popen, PIPE
import _thread

class command():
    def __init__(self):
        pass
    def initialize(self, environment, scriptPath=''):
        self.env = environment
        self.scriptPath = scriptPath
    def shutdown(self):
        pass
    def getDescription(self):
        return _('script: {0} fullpath: {1}').format(os.path.basename(self.scriptPath), self.scriptPath)
    def run(self):
        if not os.path.exists(self.scriptPath):
            self.env['runtime']['outputManager'].presentText(_('Script file not found'), soundIcon='', interrupt=False)
            return   
        if not os.path.isfile(self.scriptPath):
            self.env['runtime']['outputManager'].presentText(_('Script source is not a valid file'), soundIcon='', interrupt=False)
            return      
        if not os.access(self.scriptPath, os.X_OK):
            self.env['runtime']['outputManager'].presentText(_('Script file is not executable'), soundIcon='', interrupt=False)
            return                            
        _thread.start_new_thread(self._threadRun , ())

    def _threadRun(self):
        try:
            callstring = self.scriptPath + ' ' + self.env['general']['currUser']
            p = Popen(callstring , stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = p.communicate()
            stdout = stdout.decode('utf-8')
            stderr = stderr.decode('utf-8')
            self.env['runtime']['outputManager'].interruptOutput()
            if stderr != '':
                self.env['runtime']['outputManager'].presentText(str(stderr) , soundIcon='', interrupt=False)
            if stdout != '':
                self.env['runtime']['outputManager'].presentText(str(stdout) , soundIcon='', interrupt=False)
        except Exception as e:
                self.env['runtime']['outputManager'].presentText(e , soundIcon='', interrupt=False)
        
    def setCallback(self, callback):
        pass

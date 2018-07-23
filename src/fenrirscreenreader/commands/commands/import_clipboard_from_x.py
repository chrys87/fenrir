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
        return _("imports the graphical clipboard to Fenrir's clipboard")
    def run(self):                       
       _thread.start_new_thread(self._threadRun , ())

    def _threadRun(self):
        try:
            xClipboard = ''
            for display in range(10):
                p = Popen('su ' + self.env['general']['currUser'] + ' -c  "xclip -d :0 -o"' , stdout=PIPE, stderr=PIPE, shell=True)
                stdout, stderr = p.communicate()
                self.env['runtime']['outputManager'].interruptOutput()
                stderr = stderr.decode('utf-8')
                xClipboard = stdout.decode('utf-8')
                if (stderr == ''):
                    break      

            if stderr != '':
                self.env['runtime']['outputManager'].presentText(stderr , soundIcon='', interrupt=False)
            else:
                self.env['runtime']['memoryManager'].addValueToFirstIndex('clipboardHistory', xClipboard)
                self.env['runtime']['outputManager'].presentText('Import to Clipboard', soundIcon='CopyToClipboard', interrupt=True)
                self.env['runtime']['outputManager'].presentText(xClipboard, soundIcon='', interrupt=False)               
        except Exception as e:
            self.env['runtime']['outputManager'].presentText(e , soundIcon='', interrupt=False)
        
    def setCallback(self, callback):
        pass

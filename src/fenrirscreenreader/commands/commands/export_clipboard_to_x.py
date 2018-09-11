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
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getDescription(self):
        return _('Export current fenrir clipboard to X or GUI clipboard')
    def run(self):                       
       _thread.start_new_thread(self._threadRun , ())

    def _threadRun(self):
        try:
            if self.env['runtime']['memoryManager'].isIndexListEmpty('clipboardHistory'):
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                return 
            clipboard = self.env['runtime']['memoryManager'].getIndexListElement('clipboardHistory')                               
            for display in range(10):
                p = Popen('su ' + self.env['general']['currUser'] + ' -c  "echo -n \\\"' + clipboard.replace('"','\\\\\\"')  +'\\\" | xclip -d :' + str(display) + ' -selection c"' , stdout=PIPE, stderr=PIPE, shell=True)
                stdout, stderr = p.communicate()
                self.env['runtime']['outputManager'].interruptOutput()
                #screenEncoding = self.env['runtime']['settingsManager'].getSetting('screen', 'encoding')
                stderr = stderr.decode('utf-8')
                stdout = stdout.decode('utf-8')
                if (stderr == ''):
                    break      
            #stderr = stderr.decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
            #stdout = stdout.decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
            if stderr != '':
                self.env['runtime']['outputManager'].presentText(stderr , soundIcon='', interrupt=False)
            else:
                self.env['runtime']['outputManager'].presentText('exported to the X session.', interrupt=True)                
        except Exception as e:
            self.env['runtime']['outputManager'].presentText(e , soundIcon='', interrupt=False)
        
    def setCallback(self, callback):
        pass

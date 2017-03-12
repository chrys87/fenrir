#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
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
        return _('export the current fenrir clipboard to X clipboard')
    def run(self):                       
       print('drin')
       _thread.start_new_thread(self._threadRun , ())

    def _threadRun(self):
        print('jo')
        try:
            currClipboard = self.env['commandBuffer']['currClipboard']
            print(currClipboard)
            
            if currClipboard < 0:
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                print('1')
                return
            if not self.env['commandBuffer']['clipboard']:
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                print('2')
                return
            if not self.env['commandBuffer']['clipboard'][currClipboard]:
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                print('3')
                return 
            if self.env['commandBuffer']['clipboard'][currClipboard] == '':
                self.env['runtime']['outputManager'].presentText(_('clipboard empty'), interrupt=True)
                print('4')
                return                                         
            print('doit')
            p = Popen('su -c "echo -n \"' + self.env['commandBuffer']['clipboard'][currClipboard] +'\" | xclip -d :0 -selection c' + self.env['generalInformation']['currUser'] , stdout=PIPE, stderr=PIPE, shell=True)
            stdout, stderr = p.communicate()
            self.env['runtime']['outputManager'].interruptOutput()
            screenEncoding = self.env['runtime']['settingsManager'].getSetting('screen', 'encoding')
            stderr = stderr.decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
            stdout = stdout.decode(screenEncoding, "replace").encode('utf-8').decode('utf-8')
            print('test:',stderr,stdout)
            if stderr != '':
                self.env['runtime']['outputManager'].presentText(stdout , soundIcon='', interrupt=False)
            else:
                self.env['runtime']['outputManager'].presentText('export clipboard', soundIcon='PasteClipboardOnScreen', interrupt=True)                
        except Exception as e:
                print(e)
                self.env['runtime']['outputManager'].presentText(e , soundIcon='', interrupt=False)
        
    def setCallback(self, callback):
        pass

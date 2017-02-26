#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

generalInformation = {
'running': True,
'tutorialMode': False,
'currUser':'',
'prevUser':'',
'managerList':['punctuationManager','cursorManager','applicationManager','commandManager'
  ,'screenManager','inputManager','outputManager','debug'],
'commandFolderList':['commands','onInput','onScreenUpdate','onScreenChanged'
  ,'onApplicationChange','onSwitchApplicationProfile',],
}

#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

generalData = {
'running': True,
'args': None,
'tutorialMode': False,
'currUser':'',
'prevUser':'',
'managerList':['eventManager','punctuationManager','cursorManager','applicationManager','commandManager'
  ,'screenManager','inputManager','outputManager','debug'],
'commandFolderList':['commands','onInput','onScreenUpdate','onScreenChanged'
  ,'onApplicationChange','onSwitchApplicationProfile',],
}

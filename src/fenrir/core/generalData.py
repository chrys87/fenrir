#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug

generalData = {
'args': None,
'tutorialMode': False,
'currUser':'',
'prevUser':'',
'managerList':['eventManager','punctuationManager','cursorManager','applicationManager','commandManager'
  ,'screenManager','inputManager','outputManager','debug'],
'commandFolderList':['commands','onInput','onScreenUpdate','onScreenChanged','onHeartBeat', 'onPlugInputDevice'
  ,'onApplicationChange','onSwitchApplicationProfile',],
}

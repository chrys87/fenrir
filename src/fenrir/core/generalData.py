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
'managerList':['processManager','eventManager','punctuationManager','cursorManager','applicationManager','commandManager'
  ,'screenManager','inputManager','outputManager','helpManager','debug'],
'commandFolderList':['commands','onInput', 'onCursorChange', 'onScreenUpdate','onScreenChanged','onHeartBeat', 'onPlugInputDevice'
  ,'onApplicationChange','onSwitchApplicationProfile','help',],
}

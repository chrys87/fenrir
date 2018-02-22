#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrir.core import debug

generalData = {
'args': None,
'tutorialMode': False,
'currUser':'',
'prevUser':'',
'managerList':['processManager','punctuationManager','cursorManager','applicationManager','commandManager'
  ,'screenManager','inputManager','outputManager','helpManager','eventManager','debug'],
'commandFolderList':['commands','onInput', 'onCursorChange', 'onScreenUpdate','onScreenChanged','onHeartBeat', 'onPlugInputDevice'
  ,'onApplicationChange','onSwitchApplicationProfile','help',],
}

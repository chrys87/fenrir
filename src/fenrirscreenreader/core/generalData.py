#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

generalData = {
'args': None,
'tutorialMode': False,
'currUser':'',
'prevUser':'',
'managerList':['processManager', 'punctuationManager', 'byteManager', 'cursorManager', 'applicationManager', 'commandManager'
  , 'screenManager', 'inputManager','outputManager', 'helpManager', 'memoryManager', 'eventManager', 'debug'],
'commandFolderList':['commands','onInput', 'onCursorChange', 'onScreenUpdate','onScreenChanged','onHeartBeat', 'onPlugInputDevice'
  ,'onApplicationChange','onSwitchApplicationProfile','help',],
}

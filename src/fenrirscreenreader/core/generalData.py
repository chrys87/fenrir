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
'managerList':[ 'attributeManager','punctuationManager', 'byteManager', 'cursorManager', 'applicationManager', 'commandManager'
  , 'screenManager', 'inputManager','outputManager', 'helpManager', 'memoryManager', 'eventManager','processManager', 'debug'],
'commandFolderList':['commands','onKeyInput', 'onByteInput', 'onCursorChange', 'onScreenUpdate','onScreenChanged','onHeartBeat', 'onPlugInputDevice'
  ,'onApplicationChange','onSwitchApplicationProfile','help','vmenu-navigation',],
}

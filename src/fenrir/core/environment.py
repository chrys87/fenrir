#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from core.settingsData import settingsData
from core.runtimeData import runtimeData
from core.screenData import screenData
from core.outputData import outputData
from core.generalData import generalData
from core import commandData
from core.inputData import inputData
from core.punctuationData import punctuationData

environment = {
'screen': screenData,
'runtime': runtimeData,
'general': generalData,
'settings': settingsData,
'commands': commandData.commands,
'commandsIgnore': commandData.commandsIgnore,
'commandInfo': commandData.commandInfo,
'commandBuffer': commandData.commandBuffer,
'input': inputData,
'punctuation': punctuationData,
'output': outputData,
'soundIcons': {},
'bindings': {},
}

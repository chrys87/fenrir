#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrir.core import debug
from fenrir.core.settingsData import settingsData
from fenrir.core.runtimeData import runtimeData
from fenrir.core.screenData import screenData
from fenrir.core.outputData import outputData
from fenrir.core.generalData import generalData
from fenrir.core import commandData
from fenrir.core.inputData import inputData
from fenrir.core.punctuationData import punctuationData

environment = {
'screen': screenData,
'runtime': runtimeData,
'general': generalData,
'settings': settingsData,
'commandInfo': commandData.commandInfo,
'commandBuffer': commandData.commandBuffer,
'input': inputData,
'punctuation': punctuationData,
'output': outputData,
'soundIcons': {},
'bindings': {},
}

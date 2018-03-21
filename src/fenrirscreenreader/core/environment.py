#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.settingsData import settingsData
from fenrirscreenreader.core.runtimeData import runtimeData
from fenrirscreenreader.core.screenData import screenData
from fenrirscreenreader.core.outputData import outputData
from fenrirscreenreader.core.generalData import generalData
from fenrirscreenreader.core import commandData
from fenrirscreenreader.core.inputData import inputData
from fenrirscreenreader.core.punctuationData import punctuationData

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

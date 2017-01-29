#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from core import settings
from core import runtime
from core import screenData
from core import output
from core import generalInformation
from core import commands
from core import inputEvent
from core import punctuation

environment = {
'screenData': screenData.screenData,
'runtime': runtime.runtime,
'generalInformation': generalInformation.generalInformation,
'settings': settings.settings,
'commands': commands.commands,
'commandsIgnore': commands.commandsIgnore,
'commandInfo': commands.commandInfo,
'commandBuffer': commands.commandBuffer,
'input': inputEvent.input,
'punctuation': punctuation.punctuation,
'output': output.output,
'soundIcons': {},
'bindings': {},
}

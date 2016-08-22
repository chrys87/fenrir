#!/bin/python

from core import settings
from core import runtime
from core import screenData
from core import generalInformation
from core import commands
from core import input

environment = {
'screenData': screenData.screenData,
'runtime': runtime.runtime,
'generalInformation': generalInformation.generalInformation,
'settings': settings.settings,
'commands': commands.commands,
'commandInfo': commands.commandInfo,
'commandBuffer': commands.commandBuffer,
'input': input.input,
'soundIcons': {},
'bindings': {},
}

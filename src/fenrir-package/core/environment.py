#!/bin/python

from core import settings
from core import soundIcons
from core import bindings
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
'bindings': bindings.bindings,
'commands': commands.commands,
'input': input.input,
'commandInfo': commands.commandInfo,
'soundIcons': soundIcons.soundIcons,
}

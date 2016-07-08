#!/bin/python

from core import settings
from core import soundIcons
from core import bindings
from core import runtime
from core import screenData
from core import generalInformation

environment = {
'screenData' = screenData.screenData,
'runtime' = runtime.runtime,
'generalInformation' = generalInformation.generalInformation,
'settings' = settings.settings,
'bindings' = bindings.bindings,
'soundIcons' = soundIcons.soundIcons,
'autospeak' = ['speak_delta']
}

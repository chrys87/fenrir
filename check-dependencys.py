#!/bin/env python3
import os, sys

# default installation
# core
# speech: speech-dispatcher
# sound: sox
# braille: brltty:
defaultInstallation = ['FenrirCore','vcsaDriver','brlapiDriver','evdevDriver','speechdDriver', 'genericDriver']
currentInstallation = []

print('checking dependencys...')
# CORE
print('')
print('fenrir core:')
available = True
try:
    from daemonize import Daemonize
    print('python3-daemonize: OK')
except:
    print('python3-daemonize: FAIL')
    available = available and False
    
try:
    import enchant
    print('pyenchant: OK')
except:
    print('pyenchant: FAIL')
    available = available and False
    
if available:
    currentInstallation.append('FenrirCore')
    
# SCREEN
print('')
print('screen driver')
# VCSA (screen driver)
print('vcsaDriver')
available = True
try:
    import dbus
    print('python3-dbus: OK')
except:
    print('python3-dbus: FAIL')
    available = available and False
if os.path.exists('/dev/vcsa'):
    print('VCSA Device: OK')
else:    
    print('VCSA Device: FAIL')
    available = available and False    
if available:
    currentInstallation.append('vcsaDriver')

# BRAILLE
print('')
print('braille driver')
# brltty (braille driver)
print('brlapiDriver')
available = True
try:
    import brlapi
    print('python3-brlapi: OK')
except:
    print('python3-brlapi: FAIL')
    available = available and False
    
if available:
    currentInstallation.append('brlapiDriver')
# INPUT
print('')
print('input driver')
# evdev (input driver)
print('evdevDriver')
available = True
try:
    import evdev
    from evdev import InputDevice, UInput
    print('python3-evdev: OK')
except:
    print('python3-evdev: FAIL')
    available = available and False    
if available:
    currentInstallation.append('evdevDriver')
# SOUND
print('')
print('sound driver')
print('genericDriver (uses sox by default)')
available = True
if os.path.exists('/usr/bin/play') and os.path.exists('/usr/bin/sox'):
    print('sox: OK')
else:
    print('sox: FAIL')
    available = available and False    
if available:
    currentInstallation.append('genericDriver')
# gstreamer (sound driver)
print('gstreamerDriver')
available = True
try:
    import gi
    print('gi: OK')
except:
    print('gi: FAIL')
    available = available and False    
try:
    from gi.repository import GLib 
    print('gi GLib: OK')
except:
    print('gi GLib: FAIL')
    available = available and False    
try:
    gi.require_version('Gst', '1.0')
    from gi.repository import Gst
    print('gi Gst: OK')
except:
    print('gi Gst: FAIL')   
    available = available and False     
if available:
    currentInstallation.append('gstreamerDriver')

# SPEECH
print('')
print('speech driver')
# speechd (speech driver)
print('speechdDriver')
available = True
try:
    import speechd
    print('python3-speechd: OK')
except:
    print('python3-speechd: FAIL')
    available = available and False    
if available:
    currentInstallation.append('speechdDriver')
# espeak (speech driver)
print('espeakDriver')
available = True
try:
    from espeak import espeak 
    print('python3-espeak: OK')
except:
    print('python3-espeak: FAIL')
    available = available and False    
if available:
    currentInstallation.append('espeakDriver')    

# SUMMERY
print('')
available = True
missing = []
for element in  defaultInstallation:
    if not element in currentInstallation:
        available = False
        missing.append(element)
if available:
    print('Default Setup: OK')
else:
    print('Default Setup: FAIL')    
    print('Unavailable Default Modules:')
    for e in missing:
        print(e)
    print('you may need to install the missing dependencys for the modules above or reconfigure fenrir to not use them')
print('')
print('Available Modules:')   
for element in  currentInstallation:
    print(element)


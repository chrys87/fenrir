#!/bin/python
import evdev
from evdev import InputDevice
from select import select
import time

#devices = map(evdev.InputDevice, (evdev.list_devices()))
devices = map(evdev.InputDevice, (['/dev/input/event0','/dev/input/event1','/dev/input/event10','/dev/input/event11','/dev/input/event12','/dev/input/event14','/dev/input/event15','/dev/input/event2','/dev/input/event3','/dev/input/event4','/dev/input/event5','/dev/input/event7','/dev/input/event8','/dev/input/event9']))
devicesNew = {}
for dev in devices:
    try:
        devicesNew[dev.fd] = dev
        print('DONE: Devicename:'+ devicesNew[dev.fd].name + '  Devicepath:' + devicesNew[dev.fd].fn )
    except Exception as e:
        print('ERROR:'+ ' ' + str(e) )
    
for fd in devicesNew:
    print('Devicename:'+ devicesNew[fd].name + '  Devicepath:' + devicesNew[fd].fn )

#--- log events---
#while True:
#    r, w, x = select(devices, [], [])
#    if r != []:
#        for fd in r:
#            for event in devices[fd].read():
#                   print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + '  Events:' + str(devices[fd].active_keys(verbose=True)) + '  Value:' + str(event.value))


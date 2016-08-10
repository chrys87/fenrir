#!/bin/python
import evdev
from evdev import InputDevice, UInput
from select import select
import time

iDevices = map(evdev.InputDevice, (evdev.list_devices()))
iDevices = {dev.fd: dev for dev in iDevices if dev.fn in ['/dev/input/event18']}
uDevices = {}
for fd in iDevices:
    dev = iDevices[fd]
    uDevices[fd] = UInput()
    dev.grab()

#      dev.capabilities(),
#      dev.name,
#      dev.info.vendor,
#      dev.info.product,
#      dev.version,
#      dev.info.bustype,
#      '/dev/uinput'
#      )


i = 0
while  i < 10:
    r, w, x = select(iDevices, [], [])
    if r != []:
        i += 1
        for fd in r:
            for event in iDevices[fd].read():
                if event.code != 30:
                    uDevices[fd].write_event(event)
                    uDevices[fd].syn()
                       #print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + '  Events:' + str(devices[fd].active_keys(verbose=True)) + '  Value:' + str(event.value))

for fd in iDevices:
    iDevices[fd].ungrab()



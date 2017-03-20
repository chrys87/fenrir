#!/bin/python
import evdev
from evdev import InputDevice, UInput
from select import select
import time

iDevices = map(evdev.InputDevice, (evdev.list_devices()))
iDevices = {dev.fd: dev for dev in iDevices if evdev.events.EV_KEY in dev.capabilities()}

uDevices = {}
for fd in iDevices:
    dev = iDevices[fd]
    cap = dev.capabilities()
    del cap[0]
    uDevices[fd] = UInput(
      cap,
      dev.name,
      dev.info.vendor,
#      dev.info.product,
#      dev.version,
#      dev.info.bustype,
 #     '/dev/uinput'
      )
    dev.grab()


i = 0
while  i < 100:
    r, w, x = select(iDevices, [], [])
    if r != []:
        i += 1
        for fd in r:
            for event in iDevices[fd].read():
                if event.code != 30:  # a
                    print(event)
                    uDevices[fd].write_event(event)
                    uDevices[fd].syn()
                       #print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + '  Events:' + str(devices[fd].active_keys(verbose=True)) + '  Value:' + str(event.value))
                else:
                    print('this key is consumed')

for fd in iDevices:
    iDevices[fd].ungrab()
    iDevices[fd].close()
    uDevices[fd].close()


iDevices.clear()
uDevices.clear()




#!/bin/python
import evdev
from evdev import InputDevice, UInput
from select import select
import time

iDevices = map(evdev.InputDevice, (evdev.list_devices()))
iDevices = {dev.fd: dev for dev in iDevices}
print('----------------------')
for fd in iDevices:
    dev = iDevices[fd]
    cap = dev.capabilities()
    print('Name: ' + str(dev.name))
    print('LEDs: ' + str(dev.leds()))
    print('Has Keys: '+ str(evdev.events.EV_KEY in cap))
    if evdev.events.EV_KEY in cap:
        print('No. of keys: ' + str(len(cap[evdev.events.EV_KEY])))
        print('has Key 116: ' + str(116 in cap[evdev.events.EV_KEY]))
    print('Is Mouse: ' + str(((evdev.events.EV_REL in cap) or (evdev.events.EV_ABS in cap))))
    print('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    print(dev.capabilities(verbose=True))
    print('----------------------')


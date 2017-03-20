#!/bin/python
import evdev
from evdev import InputDevice, UInput
from select import select
import time

iDevices = map(evdev.InputDevice, (evdev.list_devices()))
iDevices = {dev.fd: dev for dev in iDevices}

for fd in iDevices:
    dev = iDevices[fd]
    cap = dev.capabilities()
    print(dev.name,dev.leds(),'has keys:'+str(evdev.events.EV_KEY in cap),'is mouse:'+str(((evdev.events.EV_REL in cap) or (evdev.events.EV_ABS in cap))))

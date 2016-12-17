#!/bin/python
import evdev
from evdev import InputDevice
from select import select
import time

devices = map(evdev.InputDevice, (evdev.list_devices()))
devices = {dev.fd: dev for dev in devices}

for fd in devices:
    for i in devices[fd].capabilities(True):
        print(devices[fd].fn,devices[fd].name,i)
while True:
    r, w, x = select(devices, [], [])
    if r != []:
        for fd in r:
            for event in devices[fd].read():
                   print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + '  EventType: '  + str(event.type) +  ' Events:' + str(devices[fd].active_keys(verbose=True)) + '  Value:' + str(event.value))



#!/bin/python
import evdev
from evdev import InputDevice
from select import select
import time

deviceList = evdev.list_devices()
readableDevices = []
for dev in deviceList:
    try:
        open(dev)
        readableDevices.append(dev)
        print('OK '+dev)
    except Exception as e:
        print('skip ' + dev + ' Error ' + str(e))
        

devices = map(evdev.InputDevice, (readableDevices))
devices = {dev.fd: dev for dev in devices}

while True:
    r, w, x = select(devices, [], [])
    if r != []:
        for fd in r:
            for event in devices[fd].read():
                   print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + '  Events:' + str(devices[fd].active_keys(verbose=True)) + '  Value:' + str(event.value))



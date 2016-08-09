import evdev
from evdev import InputDevice
from select import select
import time

devices = map(evdev.InputDevice, (evdev.list_devices()))
devices = {dev.fd: dev for dev in devices}

while True:
    r, w, x = select(devices, [], [])
    if r != []:
        for fd in r:
            for event in devices[fd].read():
                   print('Devicename:'+ devices[fd].name + '  Devicepath:' + devices[fd].fn + '  Events:' + str(devices[fd].active_keys(verbose=True)) + '  Value:' + str(event.value))


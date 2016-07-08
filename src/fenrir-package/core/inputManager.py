#!/bin/python

import evdev
from evdev import InputDevice
from select import select

class inputManager():
    def __init__(self):
        self.devices = map(evdev.InputDevice, (evdev.list_devices()))
        self.devices = {dev.fd: dev for dev in self.devices}
        for dev in self.devices.values(): print(dev)

    def getShortcutCommand(self, environment, shortcuts):
        if not shortcuts:
            return ''
        return ''

    def getKeyPressed(self, environment):
        r, w, x = select(self.devices, [], [])
        for fd in r:
            for event in self.devices[fd].read():
                if event.type == evdev.ecodes.EV_KEY:
                    print(evdev.categorize(event))
        return environment

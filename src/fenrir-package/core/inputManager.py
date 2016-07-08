#!/bin/python

import evdev
from evdev import InputDevice
from select import select

class inputManager():
    def __init__(self):
        self.devices = map(evdev.InputDevice, (evdev.list_devices()))
        self.devices = {dev.fd: dev for dev in self.devices}
        for dev in self.devices.values(): print(dev)

    def getKeyPressed(self, environment):
        r, w, x = select(self.devices, [], [])
        currShortcut = environment['input']['currShortcut']
        for fd in r:
            for event in self.devices[fd].read():
                if event.type == evdev.ecodes.EV_KEY:
                    if event.value != 0:
                        currShortcut[str(event.code)] = event.value
                    else:
                        del(currShortcut[str(event.code)])
        environment['input']['currShortcut'] = currShortcut
        environment['input']['currShortcutString'] = self.getShortcutString(environment)
        return environment

    def getShortcutString(self, environment):
        if environment['input']['currShortcut'] == {}:
            return '' 
        currShortcutStringList = []
        for key in sorted(environment['input']['currShortcut'] ):
            currShortcutStringList.append("%s-%s" % (environment['input']['currShortcut'][key], key))
        return str(currShortcutStringList)[1:-1].replace(" ","").replace("'","")

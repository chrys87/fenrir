#!/bin/python

import evdev
from evdev import InputDevice
from select import select

class inputManager():
    def __init__(self):
        self.devices = map(evdev.InputDevice, (evdev.list_devices()))
        self.devices = {dev.fd: dev for dev in self.devices}
        #for dev in self.devices.values(): print(dev)

    def getKeyPressed(self, environment):
        timeout = True
        try:
            r, w, x = select(self.devices, [], [], environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'screen', 'screenUpdateDelay'))
            environment['runtime']['globalLock'].acquire(True)
            if r != []:
                timeout = False
                for fd in r:
                    for event in self.devices[fd].read():
                        if event.type == evdev.ecodes.EV_KEY:
                            if event.value != 0:
                                environment['input']['currShortcut'][str(event.code)] = 1 #event.value
                            else:
                                try:
                                    del(environment['input']['currShortcut'][str(event.code)])
                                except:
                                    pass
        except:
            pass
        environment['input']['currShortcutString'] = self.getShortcutString(environment)
        return environment, timeout

    def getShortcutString(self, environment):
        if environment['input']['currShortcut'] == {}:
            return '' 
        currShortcutStringList = []
        for key in environment['input']['currShortcut']:
            currShortcutStringList.append("%s-%s" % (environment['input']['currShortcut'][key], key))
        currShortcutStringList = sorted(currShortcutStringList)
        return str(currShortcutStringList)[1:-1].replace(" ","").replace("'","")


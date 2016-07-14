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
        try:
            r, w, x = select(self.devices, [], [])
            environment['runtime']['globalLock'].acquire(True)
            currShortcut = environment['input']['currShortcut']
            if r != []:
                for fd in r:
                    for event in self.devices[fd].read():
                        if event.type == evdev.ecodes.EV_KEY:
                            if event.value != 0:
                                currShortcut[str(event.code)] = event.value
                            else:
                                try:
                                    del(currShortcut[str(event.code)])
                                except:
                                    pass
        except:
            pass
        environment['input']['currShortcut'] = currShortcut
        environment['input']['currShortcutString'] = self.getShortcutString(environment)
        return environment

    def getShortcutString(self, environment):
        if environment['input']['currShortcut'] == {}:
            return '' 
        currShortcutStringList = []
        for key in environment['input']['currShortcut']:
            currShortcutStringList.append("%s-%s" % (environment['input']['currShortcut'][key], key))
        currShortcutStringList = sorted(currShortcutStringList)
        return str(currShortcutStringList)[1:-1].replace(" ","").replace("'","")

    def loadShortcuts(self, environment, kbConfigPath='../../config/keyboard/desktop.kb'):
        kbConfig = open(kbConfigPath,"r")
        while(True):
            line = kbConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","").startswith("#"):
                continue
            if line.split('#')[0].count("=") != 1:
                continue
            sepLine = line.split('#')[0].split('=')
            commandString = sepLine[1]
            keys = sepLine[0].replace(" ","").split(',')
            currShortcut = []
            validKeyString = True
            for key in keys:
                if len(key) < 3:
                    validKeyString = False
                    break
                if not key[0] in ['0','1','2']:
                    validKeyString = False
                    break
                if key[1] != '-':
                    validKeyString = False
                    break
                if key[2:] != '':
                    keyInt = self.getCodeForKeyID(key[2:])
                else:
                    validKeyString = False
                    break
                if keyInt == 0:
                    validKeyString = False
                    break
                if not validKeyString:
                    break
                else:
                    currShortcut.append(key[0] + '-' + str(keyInt))
            if validKeyString:
                keyString = ''
                for k in sorted(currShortcut):
                    if keyString != '':
                        keyString += ','
                    keyString += k
                environment['bindings'][keyString] = commandString
        kbConfig.close()
        return environment

    def getCodeForKeyID(self, keyID):
        try:
            return evdev.ecodes.ecodes[keyID.upper()]
        except:
            return 0

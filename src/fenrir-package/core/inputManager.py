#!/bin/python

import evdev
from evdev import InputDevice, UInput
from select import select
import time
from utils import debug

class inputManager():
    def __init__(self):
        self.iDevices = {}
        self.uDevices = {}
        self.getInputDevices()
        self.grabDevices()
        self.ignoreKeyRelease = 0

    def proceedInputEvents(self, environment):
        timeout = True
        if not environment['input']['keyForeward']:
            self.ignoreKeyRelease = 0
        try:
            r, w, x = select(self.iDevices, [], [], environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'screen', 'screenUpdateDelay'))
            if r != []:
                timeout = False
                for fd in r:
                    for event in self.iDevices[fd].read():
                        if self.isFenrirKey(environment, event): 
                            environment['input']['consumeKey'] = not environment['input']['keyForeward']
                        if self.isConsumeKeypress(environment):   
                            self.writeUInput(self.uDevices[fd], event)
                        keyString = ''
                        if self.isFenrirKey(environment, event):
                            keyString = 'FENRIR'
                        else:
                            keyString = str(event.code) 
                        if event.type == evdev.ecodes.EV_KEY:
                            if event.value != 0:
                                environment['input']['currShortcut'][keyString] = 1 #event.value
                            else:
                                try:
                                    del(environment['input']['currShortcut'][keyString])
                                except:
                                    pass
        except Exception as e:
            self.freeDevices()
        time.sleep(0.01)        
        environment['input']['currShortcutString'] = self.getShortcutString(environment)
        if not timeout:
            environment['input']['lastInputTime'] = time.time()
            environment['input']['consumeKey'] = environment['input']['currShortcut'] != {} and environment['input']['consumeKey']
            if (environment['input']['keyForeward'] and environment['input']['currShortcut'] == {}):
                self.ignoreKeyRelease += 1
            if self.ignoreKeyRelease >= 2: # a hack... has to bee done more clean
                environment['input']['keyForeward'] = environment['input']['keyForeward'] and not environment['input']['currShortcut'] == {}
   
        return environment, timeout

    def isConsumeKeypress(self, environment):
	    return not environment['input']['consumeKey'] or \
          environment['input']['keyForeward'] or \
          not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'grabDevices')

    def writeUInput(self, uDevice, event):
        uDevice.write_event(event)
        uDevice.syn()

    def getShortcutString(self, environment):
        if environment['input']['currShortcut'] == {}:
            return '' 
        currShortcutStringList = []
        for key in environment['input']['currShortcut']:
             currShortcutStringList.append("%s-%s" % (environment['input']['currShortcut'][key], key))
        currShortcutStringList = sorted(currShortcutStringList)
        return str(currShortcutStringList)[1:-1].replace(" ","").replace("'","")
    def isFenrirKey(self,environment, event):
        return str(event.code) in environment['input']['fenrirKey']
  
    def getInputDevices(self):
        self.iDevices = map(evdev.InputDevice, (evdev.list_devices()))
        self.iDevices = {dev.fd: dev for dev in self.iDevices if 1 in dev.capabilities()}

    def grabDevices(self):
#        if environment['runtime']['settingsManager'].getSettingAsBool(environment, 'keyboard', 'grabDevices'):
#            return
        for fd in self.iDevices:
            dev = self.iDevices[fd]
            cap = dev.capabilities()
            del cap[0]
            self.uDevices[fd] = UInput(
              cap,
              dev.name,
              #dev.info.vendor,
              #dev.info.product,
              #dev.version,
              #dev.info.bustype,
              #'/dev/uinput'
              )
            dev.grab()

    def freeDevices(self):
        for fd in self.iDevices:
            try:
                self.iDevices[fd].ungrab()
            except:
                pass
            try:
                self.iDevices[fd].close()
            except:
                pass
            try:
                self.uDevices[fd].close()
            except:
                pass

        self.iDevices.clear()
        self.uDevices.clear()

        def __del__(self):
            self.freeDevices()



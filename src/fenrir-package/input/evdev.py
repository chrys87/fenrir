#!/bin/python

import evdev
from evdev import InputDevice, UInput
from select import select
import time
from utils import debug

class input():
    def __init__(self):
        self.iDevices = {}
        self.uDevices = {}
        self.getInputDevices()
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
    def getInput(self, environment):

        try:
            r, w, x = select(self.iDevices, [], [], environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'screen', 'screenUpdateDelay'))
            if r != []:
                timeout = False
                for fd in r:
                    for event in self.iDevices[fd].read():
                        if self.isFenrirKey(environment, event): 
                            environment['input']['consumeKey'] = not environment['input']['keyForeward'] and not environment['generalInformation']['suspend']
                        if self.isConsumeKeypress(environment):
                            self.writeUInput(self.uDevices[fd], event,environment)
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
            environment['runtime']['debug'].writeDebugOut(environment,"Error while inputHandling",debug.debugLevel.ERROR)        
            environment['runtime']['debug'].writeDebugOut(environment,str(e),debug.debugLevel.ERROR)               
            self.releaseDevices()
        time.sleep(0.01)        

   
        return environment, timeout

    def writeUInput(self, uDevice, event,environment):
        uDevice.write_event(event)
        uDevice.syn()
  
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
            #dev.grab()

    def releaseDevices(self):
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
            self.releaseDevices()



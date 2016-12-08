#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import evdev
import time
from evdev import InputDevice, UInput
from select import select

from core import inputEvent
from core import debug

class driver():
    def __init__(self):
        self.iDevices = {}
        self.uDevices = {}
        self.ledDevices = {}        

    def initialize(self, environment):
        self.env = environment    
        self.getInputDevices()

    def shutdown(self):
        pass
    def getInputEvent(self):
        if not self.iDevices:
            return None
        if self.iDevices == {}:
            return None
        event = None
        r, w, x = select(self.iDevices, [], [], self.env['runtime']['settingsManager'].getSettingAsFloat('screen', 'screenUpdateDelay'))
        if r != []:
            for fd in r:
                event = self.iDevices[fd].read_one()            
                while(event):
                    self.env['input']['eventBuffer'].append( [self.iDevices[fd], self.uDevices[fd], event])
                    if event.type == evdev.events.EV_KEY:
                        if event.code != 0:
                            currMapEvent = self.env['runtime']['inputDriver'].mapEvent(event)
                            if not currMapEvent:
                                return currMapEvent
                            if currMapEvent['EventState'] in [0,1,2]:
                                return currMapEvent
                    event = self.iDevices[fd].read_one()                            
        return None

    def writeEventBuffer(self):
        for iDevice, uDevice, event in self.env['input']['eventBuffer']:
            self.writeUInput(uDevice, event)

    def clearEventBuffer(self):
        del self.env['input']['eventBuffer'][:]
                        
    def writeUInput(self, uDevice, event):
        uDevice.write_event(event)
        uDevice.syn()  
    def getInputDevices(self):
        deviceList = evdev.list_devices()
        readableDevices = []
        for dev in deviceList:
            try:
                open(dev)
                readableDevices.append(dev)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut("Skip Inputdevice : " + dev +' ' + str(e),debug.debugLevel.ERROR)                     
        self.iDevices = map(evdev.InputDevice, (readableDevices))
        self.ledDevices = map(evdev.InputDevice, (readableDevices))          
        # 3 pos absolute
        # 2 pos relative
        # 17 LEDs
        # 1 Keys
        # we try to filter out mices and other stuff here        
        if self.env['runtime']['settingsManager'].getSetting('keyboard', 'device').upper() == 'ALL':
            self.iDevices = {dev.fd: dev for dev in self.iDevices if 1 in dev.capabilities()}
            self.ledDevices = {dev.fd: dev for dev in self.ledDevices if 1 in dev.capabilities() and 17 in dev.capabilities()}     
        elif self.env['runtime']['settingsManager'].getSetting('keyboard', 'device').upper() == 'NOMICE':       
            self.iDevices = {dev.fd: dev for dev in self.iDevices if 1 in dev.capabilities() and not 3 in dev.capabilities() and not 2 in dev.capabilities()}
            self.ledDevices = {dev.fd: dev for dev in self.ledDevices if 1 in dev.capabilities() and 17 in dev.capabilities() and not 3 in dev.capabilities() and not 2 in dev.capabilities()}
        else:             
            self.iDevices = {dev.fd: dev for dev in self.iDevices if dev.name.upper() in self.env['runtime']['settingsManager'].getSetting('keyboard', 'device').upper().split(',')}
            self.ledDevices = {dev.fd: dev for dev in self.ledDevices if dev.name.upper() in self.env['runtime']['settingsManager'].getSetting('keyboard', 'device').upper().split(',')}        
            
    def mapEvent(self, event):
        if not event:
            return None
        mEvent = inputEvent.inputEvent
        try:
            mEvent['EventName'] = evdev.ecodes.keys[event.code]
            mEvent['EventValue'] = event.code
            mEvent['EventSec'] = event.sec
            mEvent['EventUsec'] = event.usec                
            mEvent['EventState'] = event.value
            return mEvent
        except Exception as e:
            return None
       
    def getLedState(self, led = 0):
        # 0 = Numlock
        # 1 = Capslock
        # 2 = Rollen
        if self.ledDevices == None:
            return False
        if self.ledDevices == {}:
            return False                   
        for fd, dev in self.ledDevices.items():
            return led in dev.leds()
        return False          
    def toggleLedState(self, led = 0):
        ledState = self.getLedState(led)
        for i in self.ledDevices:
            if ledState == 1:
                self.ledDevices[i].set_led(led , 0)
            else:
                self.ledDevices[i].set_led(led , 1)
    def grabDevices(self):
#        leve the old code until the new one is better tested    
#        for fd in self.iDevices:
#            dev = self.iDevices[fd]
#            cap = dev.capabilities()
#            del cap[0]
#            self.uDevices[fd] = UInput(
#              cap,
#              dev.name,
#              #dev.info.vendor,
#              #dev.info.product,
#              #dev.version,
#              #dev.info.bustype,
#              #'/dev/uinput'
#              )
#            dev.grab()
        for fd in self.iDevices:
            try:        
                self.uDevices[fd] = UInput.from_device(self.iDevices[fd].fn)
                self.iDevices[fd].grab()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('InputDriver evdev: grabing not possible:  ' + str(e),debug.debugLevel.ERROR) 
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



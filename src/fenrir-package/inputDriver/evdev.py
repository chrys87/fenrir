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
        event = None
        r, w, x = select(self.iDevices, [], [], self.env['runtime']['settingsManager'].getSettingAsFloat('screen', 'screenUpdateDelay'))
        if r != []:
            for fd in r:
                event = self.iDevices[fd].read_one()
                self.env['input']['eventBuffer'].append( [self.iDevices[fd], self.uDevices[fd], event])
                return self.env['runtime']['inputDriver'].mapEvent(event)
        return None

    def writeEventBuffer(self):
        for iDevice, uDevice, event in self.env['input']['eventBuffer']:
            self.writeUInput(uDevice, event)
        self.clearEventBuffer()

    def clearEventBuffer(self):
        del self.env['input']['eventBuffer'][:]
                        
    def writeUInput(self, uDevice, event):
        uDevice.write_event(event)
        uDevice.syn()
  
    def getInputDevices(self):
        # 3 pos absolute
        # 2 pos relative
        # 17 LEDs
        # 1 Keys
        # we try to filter out mices and other stuff here
        self.iDevices = map(evdev.InputDevice, (evdev.list_devices()))
        self.iDevices = {dev.fd: dev for dev in self.iDevices if 1 in dev.capabilities() and not 3 in dev.capabilities() and not 2 in dev.capabilities()}
        self.ledDevices = map(evdev.InputDevice, (evdev.list_devices()))        
        self.ledDevices = {dev.fd: dev for dev in self.ledDevices if 1 in dev.capabilities() and 17 in dev.capabilities() and not 3 in dev.capabilities() and not 2 in dev.capabilities()}     
        
    def mapEvent(self, event):
        if not event:
            return None
        mEvent = inputEvent.inputEvent
        try:
            mEvent['EventName'] = evdev.ecodes.keys[event.code].upper()
            mEvent['EventValue'] = event.code
            mEvent['EventSec'] = event.sec
            mEvent['EventUsec'] = event.usec                
            mEvent['EventState'] = event.value
            return mEvent
        except Exception as e:
            print(e)
            return None

    def getNumlock(self):
        if self.ledDevices == {}:
            return True
        if self.ledDevices == None:
            return True                      
        for fd, dev in self.ledDevices.items():
            return 0 in dev.leds()
        return True

    def getCapslock(self):
        if self.ledDevices == {}:
            return False
        if self.ledDevices == None:
            return False                      
        for fd, dev in self.ledDevices.items():
            return 1 in dev.leds()
        return False   
        
    def getScrollLock(self):
        if self.ledDevices == {}:
            return False
        if self.ledDevices == None:
            return False                      
        for fd, dev in self.ledDevices.items():
            return 2 in dev.leds()
        return False          
        
    def grabDevices(self):
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



#!/bin/python

import evdev
from evdev import InputDevice, UInput
import time
from select import select

from core import inputEvent
from utils import debug

class driver():
    def __init__(self):
        self.iDevices = {}
        self.uDevices = {}
        self.getInputDevices()
    def initialize(self, environment):
        pass
    def shutdown(self, environment):
        pass
    def getInput(self, environment):
        event = None
        r, w, x = select(self.iDevices, [], [], environment['runtime']['settingsManager'].getSettingAsFloat(environment, 'screen', 'screenUpdateDelay'))
        if r != []:
            for fd in r:
                event = self.iDevices[fd].read_one()
                return event
        return None

    def writeUInput(self, uDevice, event,environment):
        uDevice.write_event(event)
        uDevice.syn()
  
    def getInputDevices(self):
        self.iDevices = map(evdev.InputDevice, (evdev.list_devices()))
        self.iDevices = {dev.fd: dev for dev in self.iDevices if 1 in dev.capabilities()}

    def mapEvent(self,environment, event):
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



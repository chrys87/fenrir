#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

_evdevAvailable = False
_evdevAvailableError = ''
try:
    import evdev
    from evdev import InputDevice, UInput
    _evdevAvailable = True
except Exception as e:
    _evdevAvailableError = str(e)

import time
from select import select
from core import inputEvent
from core import debug

class driver():
    def __init__(self):
        self.iDevices = {}
        self.uDevices = {}
        self.ledDevices = {} 
        self._initialized = False        

    def initialize(self, environment):
        self.env = environment
        global _evdevAvailable
        self._initialized = _evdevAvailable
        if not self._initialized:
            global _evdevAvailableError
            self.env['runtime']['debug'].writeDebugOut('InputDriver: ' + _evdevAvailableError,debug.debugLevel.ERROR)         
            return
        self.getInputDevices()            

    def shutdown(self):
        if not self._initialized:
            return       
        self.releaseDevices()
    def getInputEvent(self):

        if not self.hasIDevices():
            time.sleep(0.008) # dont flood CPU        
            return None
            
        event = None
        r, w, x = select(self.iDevices, [], [], self.env['runtime']['settingsManager'].getSettingAsFloat('screen', 'screenUpdateDelay'))
        if r != []:
            for fd in r:
                try:
                    event = self.iDevices[fd].read_one()            
                except:
                    #print('jow')
                    self.removeDevice(fd)
                    return None
                foreward = False
                while(event):
                    self.env['input']['eventBuffer'].append( [self.iDevices[fd], self.uDevices[fd], event])
                    if event.type == evdev.events.EV_KEY:
                        if event.code != 0:
                            currMapEvent = self.mapEvent(event)
                            if not currMapEvent:
                                foreward = True                            
                                event = self.iDevices[fd].read_one()                               
                                continue
                            if not isinstance(currMapEvent['EventName'], str):
                                foreward = True                            
                                event = self.iDevices[fd].read_one()                               
                                continue
                            if not foreward:
                                if currMapEvent['EventState'] in [0,1,2]:
                                    return currMapEvent
                    else:
                        if not event.type in [0,1,4]:
                            foreward = True
                    event = self.iDevices[fd].read_one()   
                if foreward:
                    self.writeEventBuffer()
                    self.clearEventBuffer()                                                                         
        return None

    def writeEventBuffer(self):
        if not self._initialized:
            return    
        for iDevice, uDevice, event in self.env['input']['eventBuffer']:
            self.writeUInput(uDevice, event)

    def clearEventBuffer(self):
        if not self._initialized:
            return    
        del self.env['input']['eventBuffer'][:]
                        
    def writeUInput(self, uDevice, event):
        if not self._initialized:
            return    
        uDevice.write_event(event)
        uDevice.syn()  
    def getInputDevices(self):
        if not self._initialized:
            return    
        if self.iDevices != {}:
            self.releaseDevices()
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
        if not self._initialized:
            return None    
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
        if not self._initialized:
            return False    
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
        if not self._initialized:
            return None    
        ledState = self.getLedState(led)
        for i in self.ledDevices:
            if ledState == 1:
                self.ledDevices[i].set_led(led , 0)
            else:
                self.ledDevices[i].set_led(led , 1)
    def grabDevices(self):
        if not self._initialized:
            return
        for fd in self.iDevices:
            try:        
                self.uDevices[fd] = UInput.from_device(self.iDevices[fd].fn)
            except Exception as e:
                try:
                    self.env['runtime']['debug'].writeDebugOut('InputDriver evdev: compat fallback:  ' + str(e),debug.debugLevel.ERROR)         
                    dev = self.iDevices[fd]
                    cap = dev.capabilities()
                    del cap[0]
                    self.uDevices[fd] = UInput(
                      cap,
                      dev.name,
                    )
                except Exception as e:
                    self.env['runtime']['debug'].writeDebugOut('InputDriver evdev: init Uinput not possible:  ' + str(e),debug.debugLevel.ERROR)         
                    return                  
            try:
                self.iDevices[fd].grab()
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('InputDriver evdev: grabing not possible:  ' + str(e),debug.debugLevel.ERROR)         
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
#            )
#            dev.grab()
    def removeDevice(self,fd):
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
        try:
            del(self.iDevices[fd])
        except:
            pass
        try:
            del(self.uDevices[fd])
        except:
            pass                 
    def hasIDevices(self):
        if not self._initialized:
            return False
        if not self.iDevices:
            return False
        if len(self.iDevices) == 0:
            return False
        return True    
    
    def releaseDevices(self):
        if not self.hasIDevices():
            return
        devices = self.iDevices.copy()
        for fd in devices:
            self.removeDevice(fd)
        self.iDevices.clear()
        self.uDevices.clear()

    def __del__(self):
        if not self._initialized:
            return      
        self.shutdown()



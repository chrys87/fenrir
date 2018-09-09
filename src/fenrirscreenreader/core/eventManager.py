#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
from queue import Empty
import time
from multiprocessing import Queue
from multiprocessing.sharedctypes import Value
from ctypes import c_bool

class eventManager():
    def __init__(self):
        self.running =  Value(c_bool, True)
        self._eventQueue = Queue() # multiprocessing.Queue()
        self.cleanEventQueue()
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        self.cleanEventQueue()       
         
    def proceedEventLoop(self):
        event = self._eventQueue.get()
        st = time.time()
        self.eventDispatcher(event)
        #print('NET loop ' + str(time.time() - st))        
    def eventDispatcher(self, event):
        self.env['runtime']['debug'].writeDebugOut('eventManager:eventDispatcher:start: event: ' + str(event['Type']),debug.debugLevel.INFO)

        if not event:
            return
        if not event['Type']:
            return
        if event['Type'] == fenrirEventType.Ignore:
            return
        elif event['Type'] == fenrirEventType.StopMainLoop:
            self.handleStopMainLoop(event)
        elif event['Type'] == fenrirEventType.ScreenUpdate:
            self.env['runtime']['fenrirManager'].handleScreenUpdate(event)
        elif event['Type'] == fenrirEventType.KeyboardInput:
            self.env['runtime']['fenrirManager'].handleInput(event)
        elif event['Type'] == fenrirEventType.BrailleInput:
            pass            
        elif event['Type'] == fenrirEventType.PlugInputDevice:
            self.env['runtime']['fenrirManager'].handlePlugInputDevice(event)
        elif event['Type'] == fenrirEventType.BrailleFlush:
            pass            
        elif event['Type'] == fenrirEventType.ScreenChanged:
            self.env['runtime']['fenrirManager'].handleScreenChange(event)
        elif event['Type'] == fenrirEventType.HeartBeat:
            self.env['runtime']['fenrirManager'].handleHeartBeat(event)
        elif event['Type'] == fenrirEventType.ExecuteCommand:
            self.env['runtime']['fenrirManager'].handleExecuteCommand(event)
        elif event['Type'] == fenrirEventType.ByteInput:
            self.env['runtime']['fenrirManager'].handleByteInput(event)
        elif event['Type'] == fenrirEventType.RemoteIncomming:
            self.env['runtime']['fenrirManager'].handleRemoteIncomming(event)
    def isMainEventLoopRunning(self):
        return self.running.value == 1
    def startMainEventLoop(self):
        self.running.value = 1
        while( self.isMainEventLoopRunning()):
            self.proceedEventLoop()

    def handleStopMainLoop(self, event):
        self.running.value =  0
        time.sleep(0.1)
    def stopMainEventLoop(self):
        self._eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None})                                
    def cleanEventQueue(self):
        if self._eventQueue.empty():
            return
        try:
            while True:
                self._eventQueue.get_nowait()
        except Empty:
            pass
    def getEventQueue(self):
        return self._eventQueue
    def getRunning(self):
        return self.running
    def putToEventQueue(self,event, data):
        if not isinstance(event, fenrirEventType):
            return False
        self._eventQueue.put({"Type":event,"Data":data})    
        return True

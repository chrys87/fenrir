#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
from core.eventData import fenrirEventType
from queue import Empty
import time 
from multiprocessing import Process, Queue
from multiprocessing.sharedctypes import Value
from ctypes import c_bool

class eventManager():
    def __init__(self):
        self._mainLoopRunning =  Value(c_bool, True)
        self._eventProcesses = []
        self._eventQueue = Queue() # multiprocessing.Queue()
        self.cleanEventQueue()
    def initialize(self, environment):
        self.env = environment    
        self.addSimpleEventThread(fenrirEventType.HeartBeat, self.heartBeatTimer)
    def shutdown(self):
        self.terminateAllProcesses()
        self.cleanEventQueue()
    def heartBeatTimer(self):
        try:
            time.sleep(0.5)
        except:
            pass
        #self.env['runtime']['settingsManager'].getSettingAsFloat('screen', 'screenUpdateDelay')
        return time.time()
    def terminateAllProcesses(self):
        time.sleep(1)
        for proc in self._eventProcesses:
            try:
                proc.terminate()
            except Exception as e:
                print(e)            
    def proceedEventLoop(self):
        event = self._eventQueue.get()
        st = time.time()
        self.eventDispatcher(event)
        #print('NET loop ' + str(time.time() - st))        
    def eventDispatcher(self, event):
        print(event['Type'], self._eventQueue.qsize())
        if not event:
            return
        if event['Type'] == fenrirEventType.Ignore:
            return
        elif event['Type'] == fenrirEventType.StopMainLoop:
            self.handleStopMainLoop()
            return
        elif event['Type'] == fenrirEventType.ScreenUpdate:
            self.env['runtime']['fenrirManager'].handleScreenUpdate()
        elif event['Type'] == fenrirEventType.KeyboardInput:
            self.env['runtime']['fenrirManager'].handleInput()
        elif event['Type'] == fenrirEventType.BrailleInput:
            pass            
        elif event['Type'] == fenrirEventType.PlugInputDevice:
            pass            
        elif event['Type'] == fenrirEventType.BrailleFlush:
            pass            
        elif event['Type'] == fenrirEventType.ScreenChanged:
            self.env['runtime']['fenrirManager'].handleScreenChange()
        elif event['Type'] == fenrirEventType.HeartBeat:
            self.env['runtime']['fenrirManager'].handleHeartBeat()
            #print('HeartBeat at {0} {1}'.format(event['Type'], event['Data'] ))
    def isMainEventLoopRunning(self):
        return self._mainLoopRunning.value == 1
    def startMainEventLoop(self):
        self._mainLoopRunning.value = 1
        while( self.isMainEventLoopRunning()):
            st = time.time()            
            self.proceedEventLoop()
            #print('ALL loop ' + str(time.time() - st))
    def handleStopMainLoop(self):
        self._mainLoopRunning.value =  0
        time.sleep(0.1)
    def stopMainEventLoop(self, Force = False):
        if Force:
            self._mainLoopRunning.value =  0
        self._eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None})                                
    def addCustomEventThread(self, function, pargs = None, multiprocess=False):
        self._mainLoopRunning.value =  1

        if multiprocess:        
            t = Process(target=self.customEventWorkerThread, args=(self._eventQueue, function, pargs))
        else:# thread not implemented yet
            t = Process(target=self.customEventWorkerThread, args=(self._eventQueue, function, pargs))        
        self._eventProcesses.append(t)
        t.start()
    def addSimpleEventThread(self, event, function, pargs = None, multiprocess=False, runOnce = False):
        self._mainLoopRunning.value =  1
        if multiprocess:
            t = Process(target=self.simpleEventWorkerThread, args=(event, function, pargs))
        else:# thread not implemented yet
            t = Process(target=self.simpleEventWorkerThread, args=(event, function, pargs))                    
        self._eventProcesses.append(t)
        t.start()
    def cleanEventQueue(self):
        if self._eventQueue.empty():
            return
        try:
            while True:
                self._eventQueue.get_nowait()
        except Empty:
            pass        
    def putToEventQueue(self,event, data):
        if not isinstance(event, fenrirEventType):
            return False
        self._eventQueue.put({"Type":event,"Data":data})    
        return True
    def customEventWorkerThread(self, eventQueue, function, args):       
        #if not isinstance(eventQueue, Queue):
        #    return
        if not callable(function):
            return
        while self.isMainEventLoopRunning():
            try:
                if args:
                    function(self._mainLoopRunning, eventQueue, args)
                else:
                    function(self._mainLoopRunning, eventQueue)
            except Exception as e:
                print(e)

    def simpleEventWorkerThread(self, event, function, args, runOnce = False):       
        if not isinstance(event, fenrirEventType):
            return
        if not callable(function):
            return
        while self.isMainEventLoopRunning():
            Data = None
            try:
                if args != None:
                    Data = function(self._mainLoopRunning, args)                
                else:
                    Data = function()
            except Exception as e:
                pass                
                print(e)
            self.putToEventQueue(event, Data)
            if runOnce:
                break

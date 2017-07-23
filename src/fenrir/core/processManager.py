#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from core import debug
import time 
from multiprocessing import Process, Queue
from multiprocessing.sharedctypes import Value

class eventManager():
    def __init__(self):
        self._mainLoopRunning =  Value(c_bool, True)
        self._eventProcesses = []
    def initialize(self, environment):
        self.env = environment    
    def shutdown(self):
        self.terminateAllProcesses()
        self.cleanEventQueue()
    def terminateAllProcesses(self):
        time.sleep(1)
        for proc in self._eventProcesses:
            try:
                proc.terminate()
            except Exception as e:
                print(e)            
                          
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
            self._eventProcesses.append(t)            
        else:# thread not implemented yet
            t = Process(target=self.simpleEventWorkerThread, args=(event, function, pargs))                    
        t.start()

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
                self.env['runtime']['debug'].writeDebugOut('eventManager:simpleEventWorkerThread:function():' + st(e),debug.debugLevel.ERROR) 
            self.putToEventQueue(event, Data)
            if runOnce:
                break

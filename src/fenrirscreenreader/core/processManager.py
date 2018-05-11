#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from fenrirscreenreader.core.eventData import fenrirEventType
import time, signal
from threading import Thread
from multiprocessing import Process

class processManager():
    def __init__(self):
        self._Processes = []
        self._Threads = []       
    def initialize(self, environment):
        self.env = environment 
        self.running = self.env['runtime']['eventManager'].getRunning()
        self.addSimpleEventThread(fenrirEventType.HeartBeat, self.heartBeatTimer, multiprocess=True)        
    def shutdown(self):
        self.terminateAllProcesses()
        
    def terminateAllProcesses(self):
        for proc in self._Processes:
            try:
                proc.terminate()
            except KeyboardInterrupt:
                pass           
            except:
                pass
            proc.join()                
        for t in self._Threads:
            t.join()         
    def heartBeatTimer(self, active):
        try:
            time.sleep(0.5)
        except:
            pass
        return time.time()                          
    def addCustomEventThread(self, function, pargs = None, multiprocess = False, runOnce = False):      
        eventQueue = self.env['runtime']['eventManager'].getEventQueue()
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)                 
        if multiprocess:        
            t = Process(target=self.customEventWorkerThread, args=(eventQueue, function, pargs, runOnce))
            self._Processes.append(t)                        
        else:# thread not implemented yet
            t = Thread(target=self.customEventWorkerThread, args=(eventQueue, function, pargs, runOnce))        
            self._Threads.append(t)                                
        t.start()
        signal.signal(signal.SIGINT, original_sigint_handler)             
    def addSimpleEventThread(self, event, function, pargs = None, multiprocess = False, runOnce = False):
        original_sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN)             
        if multiprocess:
            t = Process(target=self.simpleEventWorkerThread, args=(event, function, pargs, runOnce))
            self._Processes.append(t)            
        else:
            t = Thread(target=self.simpleEventWorkerThread, args=(event, function, pargs, runOnce))                    
            self._Threads.append(t)                        
        t.start()
        signal.signal(signal.SIGINT, original_sigint_handler)             
    def customEventWorkerThread(self, eventQueue, function, pargs = None, runOnce = False):      
        #if not isinstance(eventQueue, Queue):
        #    return
        if not callable(function):
            return
        while self.running.value:
            try:
                if pargs:
                    function(self.running, eventQueue, pargs)
                else:
                    function(self.running, eventQueue)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('processManager:customEventWorkerThread:function('+str(function)+'):' + str(e),debug.debugLevel.ERROR) 
            if runOnce:
                break

    def simpleEventWorkerThread(self, event, function, pargs = None, runOnce = False):            
        if not isinstance(event, fenrirEventType):
            return
        if not callable(function):
            return
        while self.running.value:
            Data = None
            try:
                if pargs:
                    Data = function(self.running, pargs)                
                else:
                    Data = function(self.running)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('processManager:simpleEventWorkerThread:function('+str(function)+'):' + str(e),debug.debugLevel.ERROR) 
            self.env['runtime']['eventManager'].putToEventQueue(event, Data)
            if runOnce:
                break

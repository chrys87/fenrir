#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

#from core import debug
from threading import Thread
from queue import Queue, Empty
import time 
from enum import Enum
from _thread import allocate_lock
#from multiprocessing import Process, Queue

class fenrirEventType(Enum):
    Ignore = 0
    StopMainLoop = 1
    ScreenUpdate = 2
    KeyboardInput = 3
    BrailleInput = 4
    PlugInputDevice = 5
    BrailleFlush = 6
    ScreenChanged = 7
    def __int__(self):
        return self.value
    def __str__(self):
        return self.name


class eventQueue(Queue):
    def clear(self):
        try:
            while True:
                self.get_nowait()
        except Empty:
            pass


class eventManager():
    def __init__(self):
        self._mainLoopRunning = True
        self._eventThreads = []
        self._eventQueue = eventQueue()
        self.lock = allocate_lock()        
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        self._eventQueue.clear()
    def proceedEventLoop(self):
        event = self._eventQueue.get()
        print(event)
        return(event != fenrirEventType.StopMainLoop)
    def startMainEventLoop(self):
        while(True):
            self.proceedEventLoop()
            self.lock.acquire(True)
            if not self._mainLoopRunning:
                break
            self.lock.release()                
    def stopMainEventLoop(self):
            self.lock.acquire(True)
            self._mainLoopRunning = False
            self.lock.release()     
            self._eventQueue.put({"EVENT":fenrirEventType.StopMainLoop,"DATA":None})        
    def addEventThread(self, event, function):
        t = Thread(target=self.eventWorkerThread, args=(event, function))
        self._eventThreads.append(t)
        t.start()
    def eventWorkerThread(self, event, function):       
#        for i in range(20):
        while True:
            Data = None
            try:
                Data = function()
            except Exception as e:
                print(e)
            self._eventQueue.put({"EVENT":event,"DATA":Data})
            self.lock.acquire(True)
            if not self._mainLoopRunning:
                break
            self.lock.release()                

def p():
    time.sleep(0.5)
    #return("p")


e = eventManager()
e.addEventThread(fenrirEventType.ScreenUpdate,p)
e.addEventThread(fenrirEventType.BrailleInput,p)
e.addEventThread(fenrirEventType.PlugInputDevice,p)
e.addEventThread(fenrirEventType.ScreenChanged,p)
time.sleep(0.5)
e.addEventThread(fenrirEventType.StopMainLoop,e.stopMainEventLoop)

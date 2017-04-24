#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

#from core import debug
from queue import Empty
import time 
from enum import Enum
from multiprocessing import Process, Queue
from multiprocessing.sharedctypes import Value
from ctypes import c_bool

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


class eventManager():
    def __init__(self):
        self._mainLoopRunning =  Value(c_bool, True)
        self._eventProcesses = []
        self._eventQueue = Queue() # multiprocessing.Queue()
        self.cleanEventQueue()
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        self.terminateAllProcesses()
        self.cleanEventQueue()
    def terminateAllProcesses(self):
        for proc in self._eventProcesses:
            try:
                proc.terminate()
            except Exception as e:
                print(e)            
    def proceedEventLoop(self):
        event = self._eventQueue.get()
        self.eventDispatcher(event)
    def eventDispatcher(self, event):
        if not event:
            return
        if event['Type'] == fenrirEventType.Ignore:
            return
        elif event['Type'] == fenrirEventType.StopMainLoop:
            self._mainLoopRunning.value = 0
            return
        elif event['Type'] == fenrirEventType.ScreenUpdate:
            print('do an update')
            pass            
        elif event['Type'] == fenrirEventType.KeyboardInput:
            pass            
        elif event['Type'] == fenrirEventType.BrailleInput:
            pass            
        elif event['Type'] == fenrirEventType.PlugInputDevice:
            pass            
        elif event['Type'] == fenrirEventType.BrailleFlush:
            pass            
        elif event['Type'] == fenrirEventType.ScreenChanged:
            pass
    def startMainEventLoop(self):
        self._mainLoopRunning.value = True
        while(self._mainLoopRunning.value):
            self.proceedEventLoop()
    def stopMainEventLoop(self, Force = False):
        if Force:
            self._mainLoopRunning.value =  False
        self._eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None})                                
    def addEventThread(self, event, function):
        self._mainLoopRunning.value =  True
        t = Process(target=self.eventWorkerThread, args=(event, function))
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
    def eventWorkerThread(self, event, function):       
        if not isinstance(event, fenrirEventType):
            return
        if not callable(function):
            return
        while self._mainLoopRunning.value:
            Data = None
            try:
                Data = function()
            except Exception as e:
                print(e)
            self.putToEventQueue(event, Data)

def p():
    time.sleep(0.02)
    return("p")

i = 1
e = eventManager()
e.addEventThread(fenrirEventType.ScreenUpdate,p)
e.addEventThread(fenrirEventType.BrailleInput,p)
e.addEventThread(fenrirEventType.PlugInputDevice,p)
e.addEventThread(fenrirEventType.ScreenChanged,p)
time.sleep(1.5)
e.addEventThread(fenrirEventType.StopMainLoop,e.stopMainEventLoop)
s = time.time()
e.startMainEventLoop()
print(time.time() - s )


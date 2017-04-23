#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

#from core import debug
#from threading import Thread
#from queue import Queue, Empty
import time 
from enum import Enum
#from _thread import allocate_lock
from multiprocessing import Process, Queue, Lock
from multiprocessing.sharedctypes import Value

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

'''
class eventQueue(Queue):
    def clear(self):
        try:
            while True:
                self.get_nowait()
        except Empty:
            pass
'''

class eventManager():
    def __init__(self):
        self._mainLoopRunning =  Value('i', 1)
        self._eventProcesses = []
        self._eventQueue = Queue()
        self.lock = Lock()     
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        for proc in self._eventProcesses:
            try:
                proc.terminate()
            except Exception as e:
                print(e)
                
        #self._eventQueue.clear()
    def proceedEventLoop(self):
        event = self._eventQueue.get()
        self.eventDispatcher(event)
        print(event)
        return(event['Type'] != fenrirEventType.StopMainLoop)
    def eventDispatcher(self, event):
        if not event:
            return
        if event['Type'] == fenrirEventType.Ignore:
            pass
        elif event['Type'] == fenrirEventType.StopMainLoop:
            self._mainLoopRunning.value = 0
        elif event['Type'] == fenrirEventType.ScreenUpdate:
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
        while(True):
            if not self.proceedEventLoop():
                self._mainLoopRunning.value = 0
                break            
    def stopMainEventLoop(self, Force = False):
        if Force:
            self._mainLoopRunning.value = 0
        time.sleep(0.5)
        self._eventQueue.put({"Type":fenrirEventType.StopMainLoop,"Data":None})                                
    def addEventThread(self, event, function):
        t = Process(target=self.eventWorkerThread, args=(event, function, self._eventQueue, self.lock))
        self._eventProcesses.append(t)
        t.start()
    def eventWorkerThread(self, event, function, eventQueue, lock):       
        while True:
            Data = None
            try:
                Data = function()
                print(Data)
            except Exception as e:
                print(e)
            eventQueue.put({"Type":event,"Data":Data})
            if self._mainLoopRunning.value == 0:
                break

def p():
    time.sleep(0.5)
    return("p")


e = eventManager()
e.addEventThread(fenrirEventType.ScreenUpdate,p)
e.addEventThread(fenrirEventType.BrailleInput,p)
e.addEventThread(fenrirEventType.PlugInputDevice,p)
e.addEventThread(fenrirEventType.ScreenChanged,p)
time.sleep(0.5)
e.addEventThread(fenrirEventType.StopMainLoop,e.stopMainEventLoop)

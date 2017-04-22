#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

#from core import debug
from threading import Thread
from queue import Queue, Empty
import time 
from enum import Enum


class fenrirEventType(Enum):
    Ignore = 0
    ScreenUpdate = 1
    KeyboardInput = 2
    BrailleInput = 3
    PlugInputDevice = 4
    BrailleFlush = 5
    ScreenChanged = 6
    StopMainLoop = 7
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
        self._eventThreads = []
        self._eventQueue = eventQueue()
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        self._eventQueue.clear()
    def proceedEventLoop(self):
        event = self._eventQueue.get()
        print(event)
        return(event != fenrirEventType.StopMainLoop)
    def startMainEventLoop(self):
        while(self.proceedEventLoop()):
            pass
    def addEventThread(self, event, function):
        t = Thread(target=self.eventWorkerThread, args=(event, function))
        self._eventThreads.append(t)
        t.start()
    def eventWorkerThread(self, event, function):       
        for i in range(20):
#        while True:
            Data = function()
            self._eventQueue.put({"EVENT":event,"DATA":Data})


def p():
    time.sleep(0.2)
    return("p")


e = eventManager()
e.addEventThread(fenrirEventType.ScreenUpdate,p)
e.addEventThread(fenrirEventType.BrailleInput,p)
e.addEventThread(fenrirEventType.PlugInputDevice,p)
e.addEventThread(fenrirEventType.ScreenChanged,p)

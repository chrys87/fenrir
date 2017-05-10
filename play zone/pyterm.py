#!/bin/python3
import sys, os
import pty
import pyte

class FenrirTermStream(pyte.Stream):
    def __init__(self):
        super().__init__()
    def attach(self, screen):
        super().attach(screen)
    def feed(self, text):
        super().feed(text)        

class FenrirTermEmu():
    def __init__(self):
        self.shell = '/bin/bash'
        if 'SHELL' in os.environ:
            self.shell = os.environ['SHELL']
        self.screen = pyte.Screen(80,24)
        self.stream = FenrirTermStream()
        self.stream.attach(self.screen)
    def outputCallback(self, fd):
        data = os.read(fd, 1024)
        self.stream.feed(data.decode('UTF8'))
        # alles
        print(self.screen.display)
        # input
        print(data.decode('UTF8'))
        return data
    def inputCallback(self, fd):
        data = os.read(fd, 1024)
        return data
    def startEmulator(self):
        pty.spawn(self.shell, self.outputCallback, self.inputCallback)

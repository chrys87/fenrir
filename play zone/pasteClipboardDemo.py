#!/bin/python3
import termios
import fcntl

def injectTextToScreen(text):
    useScreen = "/dev/tty5"
    with open(useScreen, 'w') as fd:
        for c in text:
            fcntl.ioctl(fd, termios.TIOCSTI, c)

injectTextToScreen('this is a test that works')

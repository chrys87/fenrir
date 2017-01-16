#!/bin/python3
import sys, os
import pty

mode = 'wb'
shell = '/bin/bash'
if 'SHELL' in os.environ:
    shell = os.environ['SHELL']

filename = '/home/chrys/mytypescript.txt'

script = open(filename, mode)

def read(fd):
    data = os.read(fd, 1024)
    script.write(data)
    return data
    
def write(fd):
    data = os.read(fd, 1024)
    return data

pty.spawn(shell, read, write)


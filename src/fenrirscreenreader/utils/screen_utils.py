#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import getpass, time, string, select, os

def removeNonprintable(text):
    # Get the difference of all ASCII characters from the set of printable characters
    nonprintable = set([chr(i) for i in range(128)]).difference(string.printable)
    # Use translate to remove all non-printable characters
    return text.translate({ord(character):None for character in nonprintable})

def insertNewlines(string, every=64):
    return '\n'.join(string[i:i+every] for i in range(0, len(string), every))

def splitEvery(toSplit, every=64):
    return list(toSplit[i:i+every] for i in range(0, len(toSplit), every))
def createScreenEventData(content):
    eventData = {
        'bytes': content,
        'lines': content['lines'],
        'columns': content['columns'],
        'textCursor': 
            {
                'x': int( content['cursor'][0]),
                'y': int( content['cursor'][1])
            },
        'screen': content['screen'],
        'text': content['text'],
        'attributes': content['attributes'],
        'screenUpdateTime': time.time(),            
    }
    return eventData.copy() 

def hasMore(fd, timetout=0.1):
    r, _, _ = select.select([fd], [], [], timetout)
    return (fd in r) 
def hasMoreWhat(fdList, timetout=0.1):
    if not isinstance(fdList, list):
        return []  
    elif fdList == []:
        return []
    r, _, _ = select.select(fdList, [], [], timetout)
    return r
def isValidShell(shell = ''):
    if not isinstance(shell, str):
        return False
    if shell == '':
        return False
    try:
        if not os.path.isfile(shell):
            return False
        if not os.access(shell,os.X_OK):
            return False
    except:
            return False
    return True
def getShell():
    try:
        shell = os.environ["FENRIRSHELL"]
        if isValidShell(shell):                                        
            return shell
    except:
        pass        
    try:
        shell = os.environ["SHELL"]
        if isValidShell(shell):
            return shell
    except:
        pass
    try:
        if os.acess('/etc/passwd'):
            with open('/etc/passwd') as f:
                users = f.readlines()
                for user in users:
                    (username, encrypwd, uid, gid, gecos, homedir, shell) = user.split(':')
                    shell = shell.replace('\n','')
                    if username == getpass.getuser():
                        if isValidShell(shell):                            
                            return shell
    except:
        pass
    if isValidShell('/bin/bash'):
        return '/bin/bash'
    return '/bin/sh'

#!/bin/python

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import hashlib
import difflib
import textwrap
import os

oldContentBytes = bytes()
oldContentString = ''
while(True):
  vcs = open('/dev/vcs3','rb')
  newContentBytes = vcs.read()
  vcs.close()
  newContentString = str(newContentBytes.decode('cp1252').encode('utf-8'))
  newContentString = '\n'.join(textwrap.wrap(newContentString, 80)) 
#  if oldContentBytes == b'':
#    oldContentBytes = newContentBytes
#    oldContentString = newContentString
  if oldContentBytes != newContentBytes:
    os.system('killall espeak')
    print("tty3 changed")
    print("old content hash " + hashlib.sha256(str(oldContentBytes).encode('utf-8')).hexdigest())
    print("new content hash " + hashlib.sha256(str(newContentBytes).encode('utf-8')).hexdigest())
    '''
    for i, c in enumerate(newContent):
      if c != oldContent[i]:
        changedContent = newContent[i:]
        break
    '''
    diff = difflib.ndiff(oldContentString, newContentString)
    delta = ''.join(x[2:] for x in diff if x.startswith('+ '))
    print("whats new")
    print(delta)
    os.system('espeak -v de ' + '"' + delta.replace('\n','').replace('"','').replace('-','') +  '"&')
    #os.system('spd-say ' + '"' + delta.replace('\n','') + '"')

    oldContentBytes = newContentBytes
    oldContentString = newContentString


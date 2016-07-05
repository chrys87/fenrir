#!/bin/python

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import hashlib
import difflib
import textwrap
import os
import speech.es as es

runtime = {
'columns': 0,
'screenDriver': '/dev/vcsa3',
'delta': '',
'oldContentBytes': b'',
'oldContentText': '',
'oldContentAttrib': b'',
'newContentBytes': b'',
'newContentText': '',
'newContentAttrib': b'',
'speechDriverString':'es',
'speechDriver': es.speech()
}

while(True):
  vcsa = open(runtime['screenDriver'],'rb')
  runtime['newContentBytes'] = vcsa.read()
  vcsa.close()
  runtime['columns'] = int( runtime['newContentBytes'][1])
  runtime['newContentText'] = str(runtime['newContentBytes'][::2].decode('cp1252').encode('utf-8'))[7:]
  runtime['newContentAttrib'] = runtime['newContentBytes'][1::2][7:]
  print(runtime['newContentBytes'][9])
  #runtime['newContentString'] = str(runtime['newContentBytes'].decode('cp1252').encode('utf-8'))
  runtime['newContentText'] = '\n'.join(textwrap.wrap(runtime['newContentText'], runtime['columns'])) 
  if runtime['oldContentBytes'] != runtime['newContentBytes']:
    runtime['speechDriver'].stop()
    print("tty3 changed")
    
    diff = difflib.ndiff(runtime['oldContentText'], runtime['newContentText'])
    runtime['delta'] = ''.join(x[2:] for x in diff if x.startswith('+ '))
    
    #print(runtime['delta'])
    #runtime['speechDriver'].speak(runtime['delta'])

    runtime['oldContentBytes'] = runtime['newContentBytes']
    runtime['oldContentText'] = runtime['newContentText']
    runtime['oldContentTextAttrib'] = runtime['newContentAttrib']


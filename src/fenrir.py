#!/bin/python

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import hashlib
import difflib
import textwrap
import speech.es as es
import speech.sd as sd

runtime = {
'running':True,
'columns': 0,
'lines': 0,
'screenDriver': '/dev/vcsa3',
'delta': '',
'oldCursor':{'x':0,'y':0},
'oldContentBytes': b'',
'oldContentText': '',
'oldContentAttrib': b'',
'newCursor':{'x':0,'y':0},
'newContentBytes': b'',
'newContentText': '',
'newContentAttrib': b'',
'speechDriverString':'sd',
'speechDriver': sd.speech()
}

while(runtime['running']):
  # read screen
  vcsa = open(runtime['screenDriver'],'rb')
  runtime['newContentBytes'] = vcsa.read()
  vcsa.close()

  # get metadata like cursor or screensize
  runtime['lines'] = int( runtime['newContentBytes'][0])
  runtime['columns'] = int( runtime['newContentBytes'][1])
  runtime['newCursor']['x'] = int( runtime['newContentBytes'][2])
  runtime['newCursor']['y'] = int( runtime['newContentBytes'][3])

  # analyze content
  runtime['newContentText'] = str(runtime['newContentBytes'][4:][::2].decode('cp1252').encode('utf-8'))
  runtime['newContentAttrib'] = runtime['newContentBytes'][5:][::2]
  runtime['newContentText'] = '\n'.join(textwrap.wrap(runtime['newContentText'], runtime['columns'])) 
  
  # changes on the screen
  if runtime['oldContentBytes'] != runtime['newContentBytes']:
    if len(runtime['delta']) < 3:
      runtime['speechDriver'].cancel()
    print(len(runtime['delta']))
    print("tty3 changed")
    print(runtime['delta'])    
    diff = difflib.ndiff(runtime['oldContentText'], runtime['newContentText'])
    runtime['delta'] = ''.join(x[2:] for x in diff if x.startswith('+ '))
    
    runtime['speechDriver'].speak(runtime['delta'])

    # set new "old" values
    runtime['oldContentBytes'] = runtime['newContentBytes']
    runtime['oldContentText'] = runtime['newContentText']
    runtime['oldContentTextAttrib'] = runtime['newContentAttrib']
    runtime['oldCursor']['x'] = runtime['newCursor']['x']
    runtime['oldCursor']['y'] = runtime['newCursor']['y']


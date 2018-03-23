#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import string

punctuationData = {
'LEVELDICT':{
  'none': '',
  'some': '#-$~+*-/\\@',
  'most': '.,:-$~ +*-/\\@!#%^&*()[]}{<>;',
  'all': string.punctuation + ' §',
  },
'PUNCTDICT':{
  ' ':'space',
  '&':'and',
  "'":"apostrophe",
  '@':'at',
  '\\':'backslash',
  '|':'bar',
  '!':'bang',
  '^':'carrot',
  ':':'colon',
  ',':'comma',
  '-':'dash',
  '$':'dollar',
  '.':'dot',
  '>':'greater',
  '`':'grave',
  '#':'hash',
  '{':'left brace',
  '[':'left bracket',
  '(':'left paren',
  '<':'less',
  '%':'percent',
  '+':'plus',
  '?':'question',
  '"':'quote',
  ')':'right paren',
  '}':'right brace',
  ']':'right bracket',
  ';':'semicolon',
  '/':'slash',
  '*':'star',
  '~':'tilde',
  '_':'line',
  '=':'equals',
  },
'CUSTOMDICT':{
  }, 
'EMOTICONDICT':{
  ':)':'smiley',
  ';)':'winking face',
  'XD':'loool',
  ':@':'angry face',
  ':D':'lought'
  },          
}

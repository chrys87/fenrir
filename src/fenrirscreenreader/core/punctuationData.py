#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
import string
from collections import OrderedDict

punctuationData = {
'LEVELDICT':{
  'none': '',
  'some': '#-$~+*-/\\@',
  'most': '.,:-$~ +*-/\\@!#%^&*()[]}{<>;',
  'all': string.punctuation + ' §',
  },
'PUNCTDICT':{
  },
'CUSTOMDICT':OrderedDict(), 
'EMOTICONDICT':OrderedDict(),
}

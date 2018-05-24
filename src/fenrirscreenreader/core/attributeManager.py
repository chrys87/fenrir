#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class attributeManager():
    def __init__(self):
      pass
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def formatAttributes(self, attribute, attributeFormatString = None):
        if not attributeFormatString:
            attributeFormatString = self.env['runtime']['settingsManager'].getSetting('general', 'attributeFormatString')
        if not attributeFormatString:
            return ''
        if attributeFormatString == '':
            return ''
        try:
            attributeFormatString = attributeFormatString.replace('fenrirBGColor', self.env['runtime']['screenDriver'].getFenrirBGColor(attribute))
        except Exception as e:
            pass               
        try:
            attributeFormatString = attributeFormatString.replace('fenrirFGColor', self.env['runtime']['screenDriver'].getFenrirFGColor(attribute))
        except Exception as e:
            pass               
        try:
            attributeFormatString = attributeFormatString.replace('fenrirUnderline', self.env['runtime']['screenDriver'].getFenrirUnderline(attribute))
        except Exception as e:
            pass               
        try:
            attributeFormatString = attributeFormatString.replace('fenrirBold', self.env['runtime']['screenDriver'].getFenrirBold(attribute))
        except Exception as e:
            pass               
        try:
            attributeFormatString = attributeFormatString.replace('fenrirBlink', self.env['runtime']['screenDriver'].getFenrirBlink(attribute))
        except Exception as e:
            pass               
        try:
            attributeFormatString = attributeFormatString.replace('fenrirFontSize', self.env['runtime']['screenDriver'].getFenrirFontSize(attribute))                        
        except Exception as e:
            pass               
        try:
            attributeFormatString = attributeFormatString.replace('fenrirFont', self.env['runtime']['screenDriver'].getFenrirFont(attribute))        
        except Exception as e:
            pass              
return attributeFormatString

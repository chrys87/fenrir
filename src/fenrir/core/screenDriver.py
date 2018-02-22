#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.
#attrib:
#http://rampex.ihep.su/Linux/linux_howto/html/tutorials/mini/Colour-ls-6.html
#0 = black, 1 = blue, 2 = green, 3 = cyan, 4 = red, 5 = purple, 6 = brown/yellow, 7 = white. 
#https://github.com/jwilk/vcsapeek/blob/master/linuxvt.py
#blink = 5 if attr & 1 else 0
#bold = 1 if attr & 16 else 0


from fenrir.core import debug

class screenDriver():
    def __init__(self):
        self._isInitialized = False    
        self.bgColorNames = {0: _('black'), 1: _('blue'), 2: _('green'), 3: _('cyan'), 4: _('red'), 5: _('Magenta'), 6: _('brown/yellow'), 7: _('white')}
        self.fgColorNames = {0: _('Black'), 1: _('Blue'), 2: _('Green'), 3: _('Cyan'), 4: _('Red'), 5: _('Magenta'), 6: _('brown/yellow'), 7: _('Light gray'), 8: _('Dark gray'), 9: _('Light blue'), 10: ('Light green'), 11: _('Light cyan'), 12: _('Light red'), 13: _('Light magenta'), 14: _('Light yellow'), 15: _('White')}      
    def initialize(self, environment):
        self.env = environment
        self._isInitialized = True
    def shutdown(self):
        self._isInitialized = False
    def getCurrScreen(self):
        pass
    def getCurrApplication(self):
        pass
    def getSessionInformation(self):
        pass                
    def getFenrirBGColor(self, attribute):
        return ''
    def getFenrirFGColor(self, attribute):
        return ''
    def getFenrirUnderline(self, attribute):
        return ''   
    def getFenrirBold(self, attribute):
        return ''
    def getFenrirBlink(self, attribute):
        return ''
    def getFenrirFont(self, attribute):
        return ''
    def getFenrirFontSize(self, attribute):
        return ''
    def update(self, trigger='onUpdate'):
        pass
                

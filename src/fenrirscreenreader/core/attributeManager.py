#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug

class attributeManager():
    def __init__(self):
        self.setDefaultAttributes()
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def setDefaultAttributes(self):
        self.defaultAttributes = []
        self.defaultAttributes.append((
            'white', # fg
            'black', # bg
            False, # bold
            False, # italics
            False, # underscore
            False, # strikethrough
            False, # reverse
            False, # blink
            'default', # fontsize
            'default' # fontfamily
        )) #end attribute
        self.defaultAttributes.append((
            'default', # fg
            'default', # bg
            False, # bold
            False, # italics
            False, # underscore
            False, # strikethrough
            False, # reverse
            False, # blink
            'default', # fontsize
            'default' # fontfamily
        )) #end attribute         
    def isDefaultAttribute(self,attribute):           
        return attribute in self.defaultAttributes
    def formatAttributes(self, attribute, attributeFormatString = None):
        # "black",
        # "red",
        # "green",
        # "brown",
        # "blue",
        # "magenta",
        # "cyan",
        # "white",
        # "default" # white.
        # _order_
        # "fg",
        # "bg",
        # "bold",
        # "italics",
        # "underscore",
        # "strikethrough",
        # "reverse",  
        # "blink"   
        # "fontsieze"
        # "fontfamily" 
        if not attributeFormatString:
            attributeFormatString = self.env['runtime']['settingsManager'].getSetting('general', 'attributeFormatString')
        if not attributeFormatString:
            return ''
        if attributeFormatString == '':
            return ''
        if not attribute:
            return ''
        if len(attribute) != 10:
            return ''
        
        # 0 FG color (name)
        try:
            attributeFormatString = attributeFormatString.replace('fenrirFGColor', _(attribute[0]))
        except Exception as e:
            attributeFormatString = attributeFormatString.replace('fenrirFGColor', '')
        
        # 1 BG color (name)
        try:
            attributeFormatString = attributeFormatString.replace('fenrirBGColor', _(attribute[1]))
        except Exception as e:
            attributeFormatString = attributeFormatString.replace('fenrirBGColor', '')
        
        # 2 bold (True/ False)
        try:
            if attribute[2]:
                attributeFormatString = attributeFormatString.replace('fenrirBold', _('bold'))    
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirBold', '')
        
        # 3 italics (True/ False)                                       
        try:
            if attribute[3]:        
                attributeFormatString = attributeFormatString.replace('fenrirItalics', _('italic'))
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirItalics', '')
        
        # 4 underline (True/ False)
        try:
            if attribute[4]:
                attributeFormatString = attributeFormatString.replace('fenrirUnderline', _('underline'))
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirUnderline', '')
        
        # 5 strikethrough (True/ False)
        try:
            if attribute[5]:
                attributeFormatString = attributeFormatString.replace('fenrirStrikethrough', _('strikethrough'))
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirStrikethrough', '')
        
        # 6 reverse (True/ False)
        try:
            if attribute[6]:        
                attributeFormatString = attributeFormatString.replace('fenrirReverse', _('reverse'))
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirReverse', '')
        
        # 7 blink (True/ False)     
        try:
            if attribute[7]:        
                attributeFormatString = attributeFormatString.replace('fenrirBlink', _('blink'))
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirBlink', '')
        
        # 8 font size (int/ string)
        try:
            try:
                attributeFormatString = attributeFormatString.replace('fenrirFontSize', int(attribute[8]))
            except:
                pass
            try:
                attributeFormatString = attributeFormatString.replace('fenrirFontSize', str(attribute[8]))
            except:
                pass 
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirFontSize', _('default'))
        
        # 9 font family (string)
        try:
            attributeFormatString = attributeFormatString.replace('fenrirFont', attribute[9])   
        except Exception as e:
            pass
        attributeFormatString = attributeFormatString.replace('fenrirFont', _('default'))
                 
        return attributeFormatString

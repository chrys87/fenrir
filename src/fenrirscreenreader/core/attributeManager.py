#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from collections import Counter

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
    def trackHighlights(self, oldAttr, newAttr, text):
        result = ''
        currCursor = None
        
        if oldAttr == newAttr:
            return result,  currCursor
        if len(newAttr) == 0:
            return result,  currCursor
        if len(oldAttr) != len(newAttr):
            return result,  currCursor         
        
        textLines = text.split('\n')

        if len(textLines) != len(newAttr):
            print(len(textLines), len(newAttr))        
            return result,  currCursor
        print(len(textLines), len(newAttr))
        background = []

        try:
            allAttrib = [line for line in newAttr]
            print(allAttrib)
            #from collections import Counter
            #import random

            #tups = [ (1,2), (3,4), (5,6), (1,2), (3,4) ]
            #lst = Counter(tups).most_common()
            #highest_count = max([i[1] for i in lst])
            #values = [i[0] for i in lst if i[1] == highest_count]
            #random.shuffle(values)
            #print(values[0])
                    
            bgStat = Counter(newAttr).most_common(3)              
            #for i in bgStat:
            #    print(i)
            #background.append(bgStat[0][0])
            # if there is a third color add a secondary background (for dialogs for example)
            #if len(bgStat) > 2:
            #    if bgStat[1][1] > 40:
            #        background.append(bgStat[1][0])
        except Exception as e:
            print(e)
        #background.append((7,7,0,0,0,0))
        for line in range(len(newAttr)):
            if oldAttr[line] != newAttr[line]:
                for column in range(len(newAttr[line])):
                    if oldAttr[line][column] != newAttr[line][column]:
                        if not self.isDefaultAttribute(newAttr[line][column]):
                            if not currCursor:
                                currCursor = {}
                                currCursor['x'] = column
                                currCursor['y'] = line
                            result += textLines[line][column]
                result += ' '
        return result, currCursor         

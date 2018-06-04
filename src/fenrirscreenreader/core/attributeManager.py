#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

from fenrirscreenreader.core import debug
from collections import Counter

class attributeManager():
    def __init__(self):
        self.currAttributes = None
        self.prevAttributes = None
        self.currAttributeDelta = ''
        self.currAttributeCursor = None
        self.prefAttributeCursor = None
        self.initDefaultAttributes()    
        self.prevLastCursorAttribute = None            
        self.currLastCursorAttribute = None            
        
    def initialize(self, environment):
        self.env = environment  
    def shutdown(self):
        pass
    def setLastCursorAttribute(self, lastCursorAttribute):
        self.prevLastCursorAttribute = self.currLastCursorAttribute
        self.currLastCursorAttribute = lastCursorAttribute     
    def resetLastCursorAttribute(self, lastCursorAttribute):
        self.prevLastCursorAttribute = None
        self.currLastCursorAttribute = None   
    def isLastCursorAttributeChange(self):
        if self.prevLastCursorAttribute == None:
            return False
        return self.prevLastCursorAttribute != self.currLastCursorAttribute
    def getCurrAttributeCursor(self):
        return self.currAttributeCursor
    def isAttributeCursorActive(self):
        return self.currAttributeCursor != None
    def isAttributeChange(self):
        if not self.prevAttributes: 
            return False
        return self.currAttributes != self.prevAttributes
    def resetAttributeAll(self):
        self.resetAttributeDelta()
        self.resetAttributeCursor()
    def getAttributeDelta(self):       
        return self.currAttributeDelta        
    def resetAttributeDelta(self):
        self.currAttributeDelta = ''    
    def setAttributeDelta(self, currAttributeDelta):       
        self.currAttributeDelta = currAttributeDelta
    def resetAttributeCursor(self):
        self.currAttributeCursor = None
        self.prefAttributeCursor = None
    def setAttributeCursor(self, currAttributeCursor):
        self.prefAttributeCursor = self.currAttributeCursor        
        self.currAttributeCursor = currAttributeCursor.copy()
    def resetAttributes(self, currAttributes):
        self.prevAttributes = None                                    
        self.currAttributes = currAttributes        
    def setAttributes(self, currAttributes):
        self.prevAttributes = self.currAttributes                                    
        self.currAttributes = currAttributes.copy()
    def getAttributeByXY(self, x, y):
        if not self.currAttributes:
            return None
        if len(self.currAttributes) < y:
            return None
        if len(self.currAttributes[y]) < x - 1:
            return None    
        try:    
            return self.currAttributes[y][x]
        except KeyError:
            try:
                return self.defaultAttributes[0]
            except:
                pass
        return None
    def appendDefaultAttributes(self, attribute):
        if not attribute:
            return
        if len(attribute) != 10:
            return
        self.defaultAttributes.append(attribute)     
    def initDefaultAttributes(self):
        self.defaultAttributes = [None]
        self.defaultAttributes.append([
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
        ]) #end attribute              
    def isDefaultAttribute(self,attribute):
        return attribute in self.defaultAttributes
    def hasAttributes(self, cursor, update=True):
        if not cursor:
            return False
        cursorPos = cursor.copy()
        try:
            attribute = self.getAttributeByXY( cursorPos['x'], cursorPos['y'])
            
            if update:
                self.setLastCursorAttribute(attribute)            
            if not self.isLastCursorAttributeChange():
                return False

            if self.isDefaultAttribute(attribute):
                return False

        except Exception as e:
            return False
        return True

    def formatAttributes(self, attribute, attributeFormatString = ''):
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
        if attributeFormatString == '':
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
    def trackHighlights(self):
        
        result = ''
        currCursor = None
        # screen change
        if self.prevAttributes == None:
            return result,  currCursor                
        # no change
        if self.prevAttributes == self.currAttributes:
            return result,  currCursor
        # error case
        if self.currAttributes == None:
            return result,  currCursor                  
        # special case for pty if not text exists.
        if len(self.currAttributes) == 0:
            return result,  currCursor        
        text = self.env['runtime']['screenManager'].getScreenText()
        textLines = text.split('\n')

        if len(textLines) != len(self.currAttributes):
            return result,  currCursor
        #print(len(textLines), len(newAttr))
        #background = []

        try:
            pass
            #llAttrib = [line for line in newAttr]
            
            #print(Counter(allAttrib[0]).most_common())
            #from collections import Counter
            #import random

            #tups = [ (1,2), (3,4), (5,6), (1,2), (3,4) ]
            #lst = Counter(tups).most_common()
            #highest_count = max([i[1] for i in lst])
            #values = [i[0] for i in lst if i[1] == highest_count]
            #random.shuffle(values)
            #print(values[0])
                    
            #bgStat = Counter(newAttr).most_common(3)              
            #for i in bgStat:
            #    print(i)
            #background.append(bgStat[0][0])
            # if there is a third color add a secondary background (for dialogs for example)
            #if len(bgStat) > 2:
            #    if bgStat[1][1] > 40:
            #        background.append(bgStat[1][0])
        except Exception as e:
            print(e)
        for line in range(len(self.prevAttributes)):
            if self.prevAttributes[line] != self.currAttributes[line]:
                for column in range(len(self.prevAttributes[line])):
                    if self.prevAttributes[line][column] != self.currAttributes[line][column]:
                        if not self.isDefaultAttribute(self.currAttributes[line][column]):
                            if not currCursor:
                                currCursor = {'x': column, 'y': line}
                            result += textLines[line][column]
                result += ' '
        return result, currCursor         

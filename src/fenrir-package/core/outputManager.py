#!/bin/python

class outputManager():
    def __init__(self):
        pass
    def presentText(self, environment, Text, Interrupt=True):
        self.speakText(environment, Text, Interrupt)
        self.brailleText(environment, Text)

    def speakText(self, environment, Text, Interrupt=True):
        if environment['runtime']['speechDriver'] == None:
            return
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'):
            return
        if Interrupt:
            self.interruptOutput(environment)
        environment['runtime']['speechDriver'].speak(Text)

    def brailleText(self, environment, Text):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braile', 'enabled'):
            return    
        print('braille')
    def interruptOutput(self, environment):
        environment['runtime']['speechDriver'].cancel()
 
    def playSoundIcon(self, environment, Text):
        pass

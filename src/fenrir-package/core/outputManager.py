#!/bin/python

class outputManager():
    def __init__(self):
        pass
    def presentText(self, environment, text, interrupt=True, soundIconName = ''):
        self.speakText(environment, text, interrupt)
        self.brailleText(environment, text)
        self.playSoundIcon(environment, soundIconName)

    def speakText(self, environment, text, interrupt=True):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'speech', 'enabled'):
            return        
        if environment['runtime']['speechDriver'] == None:
            return
        if interrupt:
            self.interruptOutput(environment)
        environment['runtime']['speechDriver'].setLanguage(environment['runtime']['settingsManager'].getSetting(environment, 'speech', 'language'))            
        environment['runtime']['speechDriver'].setVoice(environment['runtime']['settingsManager'].getSetting(environment, 'speech', 'voice'))
        environment['runtime']['speechDriver'].setPitch(environment['runtime']['settingsManager'].getSettingAsInt(environment, 'speech', 'pitch'))
        environment['runtime']['speechDriver'].setSpeed(environment['runtime']['settingsManager'].getSettingAsInt(environment, 'speech', 'rate'))
        environment['runtime']['speechDriver'].setModule(environment['runtime']['settingsManager'].getSetting(environment, 'speech', 'module'))
        environment['runtime']['speechDriver'].setVolume(environment['runtime']['settingsManager'].getSettingAsInt(environment, 'speech', 'volume'))
        environment['runtime']['speechDriver'].speak(text)

    def brailleText(self, environment, text, interrupt=True):
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'braille', 'enabled'):
            return
        if environment['runtime']['braillehDriver'] == None:
            return        
        print('braille')
    def interruptOutput(self, environment):
        environment['runtime']['speechDriver'].cancel()
        environment['runtime']['soundDriver'].cancel()

    def playSoundIcon(self, environment, soundIconName, interrupt=True):
        if soundIconName == '':
            return
        if not environment['runtime']['settingsManager'].getSettingAsBool(environment, 'sound', 'enabled'):
            return    
        if environment['runtime']['soundDriver'] == None:
            return        
        print(soundIconName)
        try:
            print(environment['soundIcons'][soundIconName])
            environment['runtime']['soundDriver'].playSoundFile(environment, environment['soundIcons'][soundIconName], interrupt)
        except:
            print('no icon there for' + IconName)

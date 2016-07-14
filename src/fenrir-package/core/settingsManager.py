#!/bin/python
import evdev
import importlib.util
from configparser import ConfigParser
from core import inputManager
from core import commandManager
from core import environment 
from core.settings import settings
from utils import debug

class settingsManager():
    def __init__(self):
        self.settings = settings

    def loadShortcuts(self, environment, kbConfigPath='../../config/keyboard/desktop.kb'):
        kbConfig = open(kbConfigPath,"r")
        while(True):
            line = kbConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","").startswith("#"):
                continue
            if line.count("=") != 1:
                continue
            sepLine = line.split('=')
            commandString = sepLine[1]
            keys = sepLine[0].replace(" ","").split(',')
            currShortcut = []
            validKeyString = True
            for key in keys:
                if len(key) < 3:
                    validKeyString = False
                    break
                if not key[0] in ['0','1','2']:
                    validKeyString = False
                    break
                if key[1] != '-':
                    validKeyString = False
                    break
                if key[2:] != '':
                    keyInt = self.getCodeForKeyID(key[2:])
                else:
                    validKeyString = False
                    break
                if keyInt == 0:
                    validKeyString = False
                    break
                if not validKeyString:
                    break
                else:
                    currShortcut.append(key[0] + '-' + str(keyInt))
            if validKeyString:
                keyString = ''
                for k in sorted(currShortcut):
                    if keyString != '':
                        keyString += ','
                    keyString += k
                environment['bindings'][keyString] = commandString
        kbConfig.close()
        return environment

    def getCodeForKeyID(self, keyID):
        try:
            return evdev.ecodes.ecodes[keyID.upper()]
        except:
            return 0
    
    def loadSettings(self, environment, settingConfigPath='../../config/settings/settings.cfg'):
        environment['settings'] = ConfigParser()
        environment['settings'].read(settingConfigPath)
        return environment

    def getSetting(self, environment, section, setting):
        value = ''
        try:
            value = environment['settings'].get(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsInt(self, environment, section, setting):
        return int(getSetting(self, environment, section, setting))

    def getSettingAsBool(self, environment, section, setting):
        return bool(getSetting(self, environment, section, setting))  
      
    def loadSpeechDriver(self, environment, driverName):
        if environment['runtime']['speechDriver'] != None:
            environment['runtime']['speechDriver'].shutdown()    
        spec = importlib.util.spec_from_file_location(driverName, 'speech/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['speechDriver'] = driver_mod.speech()
        return environment

    def loadSoundDriver(self, environment, driverName):
        if environment['runtime']['soundDriver'] != None:
            environment['runtime']['soundDriver'].shutdown()    
        spec = importlib.util.spec_from_file_location(driverName, 'sound/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['soundDriver'] = driver_mod.sound()        
        return environment

    def loadScreenDriver(self, environment, driverName):
        spec = importlib.util.spec_from_file_location(driverName, 'screen/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['screenDriver'] = driver_mod.screen() 
        return environment        
    def initFenrirConfig(self):
        return self.reInitFenrirConfig(environment.environment)

    def reInitFenrirConfig(self, environment):

        environment['runtime']['settingsManager'] = self 
        environment['runtime']['inputManager'] = inputManager.inputManager()
        environment = environment['runtime']['settingsManager'].loadShortcuts(environment)
        environment = environment['runtime']['settingsManager'].loadSettings(environment)

        environment['runtime']['commandManager'] = commandManager.commandManager()
        environment = environment['runtime']['commandManager'].loadCommands(environment,'commands')
        environment = environment['runtime']['commandManager'].loadCommands(environment,'onInput')
        environment = environment['runtime']['commandManager'].loadCommands(environment,'onScreenChanged')
        environment['runtime']['debug'] = debug.debug()
        environment = environment['runtime']['settingsManager'].loadSpeechDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'speech', 'driver'))
        environment = environment['runtime']['settingsManager'].loadScreenDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'driver'))
        environment = environment['runtime']['settingsManager'].loadSoundDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'sound', 'driver'))
        return environment
    

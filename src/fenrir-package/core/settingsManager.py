#!/bin/python
import evdev
import importlib.util
import os
from configparser import ConfigParser
from core import inputManager
from core import outputManager
from core import commandManager
from core import screenManager
from core import environment 
from core.settings import settings
from utils import debug

class settingsManager():
    def __init__(self):
        self.settings = settings
    def initialize(self, environment):
        return environment
    def shutdown(self, environment):
        return environment
    def loadShortcuts(self, environment, kbConfigPath='../../config/keyboard/desktop.conf'):
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
            commandName = sepLine[1]
            sepLine[0] = sepLine[0].replace(" ","")
            sepLine[0] = sepLine[0].replace("'","")
            sepLine[0] = sepLine[0].replace('"',"")
            keys = sepLine[0].split(',')
            shortcutKeys = []
            shortcutRepeat = 1
            shortcut = []
            for key in keys:
                try:
                    shortcutRepeat = int(key)
                except:
                    shortcutKeys.append(key.upper()) 
            shortcut.append(shortcutRepeat)
            shortcut.append(sorted(shortcutKeys))
            print(str(shortcut))
            environment['bindings'][str(shortcut)] = commandName     
        kbConfig.close()
        return environment

    def getCodeForKeyID(self, keyID):
        try:
            return evdev.ecodes.ecodes[keyID.upper()]
        except:
            return 0

    def loadSoundIcons(self, environment, soundIconPath):
        siConfig = open(soundIconPath + '/soundicons.conf',"r")
        while(True):
            line = siConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","").startswith("#"):
                continue
            if line.count("=") != 1:
                continue
            Values = line.split('=')
            soundIcon = Values[0]
            Values[1] = Values[1].replace("'","")
            Values[1] = Values[1].replace('"',"")
            soundIconFile = ''
            if os.path.exists(Values[1]):
                soundIconFile = Values[1]
            else:
                if not soundIconPath.endswith("/"):
                    soundIconPath += '/'
                if os.path.exists(soundIconPath + Values[1]):
                    soundIconFile = soundIconPath + Values[1]
            environment['soundIcons'][soundIcon] = soundIconFile
        siConfig.close()
        return environment

    def loadSettings(self, environment, settingConfigPath):
        if not os.path.exists(settingConfigPath):
            return None
        environment['settings'] = ConfigParser()
        environment['settings'].read(settingConfigPath)
        return environment

    def setSetting(self, environment, section, setting, value):
        environment['settings'].set(section, setting, value)
        return environment

    def getSetting(self, environment, section, setting):
        value = ''
        try:
            value = environment['settings'].get(section, setting)
        except:
            value = str(self.settings[section][setting])
        return value

    def getSettingAsInt(self, environment, section, setting):
        value = 0
        try:
            value = environment['settings'].getint(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsFloat(self, environment, section, setting):
        value = 0.0
        try:
            value = environment['settings'].getfloat(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsBool(self, environment, section, setting):
        value = False
        try:
            value = environment['settings'].getboolean(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def loadDriver(self, environment, driverName, driverType):
        if environment['runtime'][driverType] != None:
            environment['runtime'][driverType].shutdown()    
        spec = importlib.util.spec_from_file_location(driverName, driverType + '/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime'][driverType] = driver_mod.driver()
        environment['runtime'][driverType].initialize(environment)           
        return environment

    def setFenrirKeys(self, environment, keys):
        keys = keys.upper()
        keyList = keys.split(',')
        for key in keyList:
            if not key in  environment['input']['fenrirKey']:
                environment['input']['fenrirKey'].append(key)
        return environment

    def keyIDasString(self, key):
        try:
            KeyID = self.getCodeForKeyID(key)
            return str(KeyID)
        except:
            return ''

    def initFenrirConfig(self, environment = environment.environment, settingsRoot = '/etc/fenrir/', settingsFile='settings.conf'):
        environment['runtime']['debug'] = debug.debug()
        if not os.path.exists(settingsRoot):
            if os.path.exists('../../config/'):
                settingsRoot = '../../config/'
            else:
                return None
               
        environment['runtime']['settingsManager'] = self    
        environment = environment['runtime']['settingsManager'].loadSettings(environment, settingsRoot + '/settings/' + settingsFile)
        if environment == None:
            return None
        environment = self.setFenrirKeys(environment, self.getSetting(environment, 'general','fenrirKeys'))
        if not os.path.exists(self.getSetting(environment, 'keyboard','keyboardLayout')):
            if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting(environment, 'keyboard','keyboardLayout')):  
                self.setSetting(environment, 'keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting(environment, 'keyboard','keyboardLayout'))
                environment = environment['runtime']['settingsManager'].loadShortcuts(environment, self.getSetting('keyboard','keyboardLayout'))
            if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting(environment, 'keyboard','keyboardLayout') + '.conf'):  
                self.setSetting(environment, 'keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting(environment, 'keyboard','keyboardLayout') + '.conf')
                environment = environment['runtime']['settingsManager'].loadShortcuts(environment, self.getSetting(environment, 'keyboard','keyboardLayout'))
        else:
            environment = environment['runtime']['settingsManager'].loadShortcuts(environment, self.getSetting(environment, 'keyboard','keyboardLayout'))
        
        if not os.path.exists(self.getSetting(environment, 'sound','theme') + '/soundicons.conf'):
            if os.path.exists(settingsRoot + 'sound/'+ self.getSetting(environment, 'sound','theme')):  
                self.setSetting(environment, 'sound', 'theme', settingsRoot + 'sound/'+ self.getSetting(environment, 'sound','theme'))
                if os.path.exists(settingsRoot + 'sound/'+ self.getSetting(environment, 'sound','theme') + '/soundicons.conf'):  
                     environment = environment['runtime']['settingsManager'].loadSoundIcons(environment, self.getSetting(environment, 'sound','theme'))
        else:
            environment = environment['runtime']['settingsManager'].loadSoundIcons(environment, self.getSetting(environment, 'sound','theme'))

        environment['runtime']['inputManager'] = inputManager.inputManager()
        environment = environment['runtime']['inputManager'].initialize(environment)             
        environment['runtime']['outputManager'] = outputManager.outputManager()
        environment = environment['runtime']['outputManager'].initialize(environment)             
        environment['runtime']['commandManager'] = commandManager.commandManager()
        environment = environment['runtime']['commandManager'].initialize(environment)  
    
        if environment['runtime']['screenManager'] == None:
            environment['runtime']['screenManager'] = screenManager.screenManager()
            environment = environment['runtime']['screenManager'].initialize(environment) 
            
            
        environment = environment['runtime']['commandManager'].loadCommands(environment,'commands')
        environment = environment['runtime']['commandManager'].loadCommands(environment,'onInput')
        environment = environment['runtime']['commandManager'].loadCommands(environment,'onScreenChanged')

        environment = environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'speech', 'driver'), 'speechDriver')
        environment = environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'driver'), 'screenDriver')
        environment = environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'sound', 'driver'), 'soundDriver')
        environment = environment['runtime']['settingsManager'].loadDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'keyboard', 'driver'), 'inputDriver') 
        environment['runtime']['debug'].writeDebugOut(environment,'\/-------environment-------\/',debug.debugLevel.ERROR)        
        environment['runtime']['debug'].writeDebugOut(environment,str(environment),debug.debugLevel.ERROR)
        environment['runtime']['debug'].writeDebugOut(environment,'\/-------settings.conf-------\/',debug.debugLevel.ERROR)        
        environment['runtime']['debug'].writeDebugOut(environment,str(environment['settings']._sections
),debug.debugLevel.ERROR)        
        return environment
     

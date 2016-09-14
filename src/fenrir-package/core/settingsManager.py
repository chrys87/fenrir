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
            commandString = sepLine[1]
            keys = sepLine[0].replace(" ","").split(',')
            currShortcut = []
            validKeyString = True
            keyIdent = ''
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
                    if key[2:] == 'FENRIR':
                        keyIdent= 'FENRIR'
                    else:
                        keyInt = self.getCodeForKeyID(key[2:])
                        keyIdent = str(keyInt)
                else:
                    validKeyString = False
                    break
                if keyIdent == '':
                    validKeyString = False
                    break                
                if not validKeyString:
                    break
                else:
                    currShortcut.append(key[0] + '-' + keyIdent)
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

    def loadSoundIcons(self, environment, soundIconPath=''):
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
            if len(Values) > 2:
                continue
            soundIcon = Values[0]
            Values[1] = Values[1].replace("'","")
            Values[1] = Values[1].replace('"',"")
            validSoundIcon = False
            FilePath = ''
            if os.path.exists(Values[1]):
                FilePath = Values[1]
                validSoundIcon = True
            else:
                if not soundIconPath.endswith("/"):
                    soundIconPath += '/'
                if os.path.exists(soundIconPath + Values[1]):
                    FilePath = soundIconPath + Values[1]
                    validSoundIcon = True
            if validSoundIcon:
                environment['soundIcons'][soundIcon] = FilePath
        siConfig.close()
        return environment

    def loadSettings(self, environment, settingConfigPath='../../config/settings/settings.conf'):
        environment['settings'] = ConfigParser()
        #if not exist what is ?????
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

    def loadSpeechDriver(self, environment, driverName):
        if environment['runtime']['speechDriver'] != None:
            environment['runtime']['speechDriver'].shutdown()    
        spec = importlib.util.spec_from_file_location(driverName, 'speech/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['speechDriver'] = driver_mod.speech()
        environment['runtime']['speechDriver'].initialize(environment)           
        return environment

    def loadSoundDriver(self, environment, driverName):
        if environment['runtime']['soundDriver'] != None:
            environment['runtime']['soundDriver'].shutdown()    
        spec = importlib.util.spec_from_file_location(driverName, 'sound/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['soundDriver'] = driver_mod.sound()
        environment['runtime']['soundDriver'].initialize(environment)           
        return environment

    def loadScreenDriver(self, environment, driverName):
        spec = importlib.util.spec_from_file_location(driverName, 'screen/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['screenDriver'] = driver_mod.screen() 
        environment['runtime']['screenDriver'].initialize(environment)
        return environment

    def loadInputDriver(self, environment, driverName):
        spec = importlib.util.spec_from_file_location(driverName, 'input/' + driverName + '.py')
        driver_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(driver_mod)
        environment['runtime']['inputDriver'] = driver_mod.input() 
        environment['runtime']['inputDriver'].initialize(environment)        
        return environment

    def setFenrirKeys(self, environment, keys):
        keyList = keys.split(',')
        for key in keyList:
            keyID = self.keyIDasString( key)
            if keyID != '':
                if not keyID in  environment['input']['fenrirKey']:
                    environment['input']['fenrirKey'].append(keyID)
        return environment

    def keyIDasString(self, key):
        try:
            KeyID = self.getCodeForKeyID(key)
            return str(KeyID)
        except:
            return ''

    def initFenrirConfig(self, environment = environment.environment, settingsRoot = '/etc/fenrir/config/', settingsFile='settings.conf'):
        if not os.path.exists(settingsRoot):
            if os.path.exists('../../config/'):
                settingsRoot = '../../config/'
            else:
                return None    
        environment['runtime']['settingsManager'] = self
        environment['runtime']['debug'] = debug.debug()        
        environment = environment['runtime']['settingsManager'].loadSettings(environment, settingsRoot + '/settings/' + settingsFile)
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

        environment = environment['runtime']['settingsManager'].loadSpeechDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'speech', 'driver'))
        environment = environment['runtime']['settingsManager'].loadScreenDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'screen', 'driver'))
        environment = environment['runtime']['settingsManager'].loadSoundDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'sound', 'driver'))
        environment = environment['runtime']['settingsManager'].loadInputDriver(environment,\
          environment['runtime']['settingsManager'].getSetting(environment,'keyboard', 'driver'))         
        environment['runtime']['debug'].writeDebugOut(environment,'\/-------environment-------\/',debug.debugLevel.ERROR)        
        environment['runtime']['debug'].writeDebugOut(environment,str(environment),debug.debugLevel.ERROR)
        environment['runtime']['debug'].writeDebugOut(environment,'\/-------settings.conf-------\/',debug.debugLevel.ERROR)        
        environment['runtime']['debug'].writeDebugOut(environment,str(environment['settings']._sections
),debug.debugLevel.ERROR)        
        return environment
     

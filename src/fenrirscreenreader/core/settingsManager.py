#!/bin/python
# -*- coding: utf-8 -*-

# Fenrir TTY screen reader
# By Chrys, Storm Dragon, and contributers.

import os, inspect

currentdir = os.path.dirname(os.path.realpath(os.path.abspath(inspect.getfile(inspect.currentframe()))))
fenrirPath = os.path.dirname(currentdir)

from configparser import ConfigParser
from fenrirscreenreader.core import debugManager
from fenrirscreenreader.core import memoryManager
from fenrirscreenreader.core import processManager
from fenrirscreenreader.core import eventManager
from fenrirscreenreader.core import inputManager
from fenrirscreenreader.core import outputManager
from fenrirscreenreader.core import commandManager
from fenrirscreenreader.core import screenManager
from fenrirscreenreader.core import punctuationManager
from fenrirscreenreader.core import cursorManager
from fenrirscreenreader.core import applicationManager
from fenrirscreenreader.core import helpManager
from fenrirscreenreader.core import vmenuManager
from fenrirscreenreader.core import textManager
from fenrirscreenreader.core import tableManager
from fenrirscreenreader.core import byteManager
from fenrirscreenreader.core import attributeManager
from fenrirscreenreader.core import barrierManager
from fenrirscreenreader.core import remoteManager
from fenrirscreenreader.core import sayAllManager
from fenrirscreenreader.core import quickMenuManager
from fenrirscreenreader.core import environment 
from fenrirscreenreader.core.settingsData import settingsData
from fenrirscreenreader.core import debug
from fenrirscreenreader.utils import module_utils

class settingsManager():
    def __init__(self):
        self.settings = settingsData
        self.settingArgDict = {}
        self.bindingsBackup = None
    def initialize(self, environment):
        self.env = environment
    def shutdown(self):
        pass
    def getBindingBackup(self):
        return self.bindingsBackup.copy()
    def loadSoundIcons(self, soundIconPath):
        siConfig = open(soundIconPath + '/soundicons.conf',"r")
        while(True):
            line = siConfig.readline()
            if not line:
                break
            line = line.replace('\n','')
            if line.replace(" ","") == '':
                continue
            if line.replace(" ","").startswith("#"):
                continue
            if line.count("=") != 1:
                continue
            Values = line.split('=')
            soundIcon = Values[0].upper()
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
            self.env['soundIcons'][soundIcon] = soundIconFile
            self.env['runtime']['debug'].writeDebugOut("SoundIcon: " + soundIcon + '.' + soundIconFile, debug.debugLevel.INFO, onAnyLevel=True)               
        siConfig.close()
    
    def loadSettings(self, settingConfigPath):
        if not os.path.exists(settingConfigPath):
            return False
        if not os.access(settingConfigPath, os.R_OK):
            return False
        self.env['settings'] = ConfigParser()
        self.env['settings'].read(settingConfigPath)
        return True
    def saveSettings(self, settingConfigPath):
        # set opt dict here
        # save file
        try:
            #print('file: ',settingConfigPath)
            for section, settings in self.settingArgDict.items():
                for setting, value in settings.items():
                    #print(section, setting, value)
                    self.env['settings'].set(section, setting, value)
            #print('full',self.env['settings'])

            configFile = open(settingConfigPath, 'w')
            self.env['settings'].write(configFile)
            configFile.close()
            os.chmod(settingConfigPath, 0o666)
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('saveSettings: save settingsfile:' + settingConfigPath + 'failed. Error:' + str(e), debug.debugLevel.ERROR)
    def setSetting(self, section, setting, value):
        self.setOptionArgDict(section, setting, value)
        #self.env['settings'].set(section, setting, value)

    def getSetting(self, section, setting):
        value = ''
        try:
            value = self.settingArgDict[section][setting]
            return value
        except:
            pass
        try:
            value = self.env['settings'].get(section, setting)
        except:
            value = str(self.settings[section][setting])
        return value

    def getSettingAsInt(self, section, setting):
        value = 0
        try:
            value = int(self.settingArgDict[section][setting])
            return value
        except Exception as e:
            pass
        try:
            value = self.env['settings'].getint(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsFloat(self, section, setting):
        value = 0.0
        try:
            value = float(self.settingArgDict[section][setting])
            return value
        except Exception as e:
            pass
        try:
            value = self.env['settings'].getfloat(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def getSettingAsBool(self, section, setting):
        value = False
        try:
            value = self.settingArgDict[section][setting].upper() in ['1','YES','JA','TRUE']
            return value
        except Exception as e:
            pass
        try:
            value = self.env['settings'].getboolean(section, setting)
        except:
            value = self.settings[section][setting]
        return value

    def loadDriver(self, driverName, driverType):
        try:
            self.env['runtime'][driverType].shutdown(self.env)
        except:
            pass
        try:
            driver_mod = module_utils.importModule(driverName,
              fenrirPath + "/" + driverType + '/' + driverName + '.py')
            self.env['runtime'][driverType] = driver_mod.driver()
            self.env['runtime'][driverType].initialize(self.env)
            self.env['runtime']['debug'].writeDebugOut('Loading Driver '  + driverType + ' (' + driverName +") OK",debug.debugLevel.INFO, onAnyLevel=True)             
        except Exception as e:
            self.env['runtime']['debug'].writeDebugOut('Loading Driver '  + driverType + ' (' + driverName +") FAILED:"+ str(e), debug.debugLevel.ERROR)        
            try:
                driver_mod = module_utils.importModule(driverName,
                  fenrirPath + "/" + driverType + '/dummyDriver.py')
                self.env['runtime'][driverType] = driver_mod.driver()
                self.env['runtime'][driverType].initialize(self.env)
            except Exception as e:
                self.env['runtime']['debug'].writeDebugOut('(fallback) Loading Driver '  + driverType + ' (dummyDriver) FAILED:'+ str(e), debug.debugLevel.ERROR)

    def shutdownDriver(self, driverType):
        try:
            self.env['runtime'][driverType].shutdown()
        except Exception as e:
            pass
        del self.env['runtime'][driverType]

    def setFenrirKeys(self, keys):
        keys = keys.upper()
        keyList = keys.split(',')
        for key in keyList:
            if not key in  self.env['input']['fenrirKey']:
                self.env['input']['fenrirKey'].append(key)
    def setScriptKeys(self, keys):
        keys = keys.upper()
        keyList = keys.split(',')
        for key in keyList:
            if not key in  self.env['input']['scriptKey']:
                self.env['input']['scriptKey'].append(key)
    def resetSettingArgDict(self):
        self.settingArgDict = {}
    def setOptionArgDict(self, section, setting, value):
        #section = section.lower()
        #setting = setting.lower()
        try:
            e = self.settingArgDict[section]
        except KeyError:
            self.settingArgDict[section] = {}
        try:
            t = self.settings[section][setting]
        except:
            print(section,setting, 'not found')
            return
        try:
            if isinstance(self.settings[section][setting], str):
                v = str(value)
            elif isinstance(self.settings[section][setting], bool):
                if not value in ['True','False']:
                    raise ValueError('could not convert string to bool: '+ value)
            elif isinstance(self.settings[section][setting], int):
                v = int(value)
            elif isinstance(self.settings[section][setting], float):
                v = float(value)
            self.settingArgDict[section][setting] = str(value)
        except Exception as e:
            print('settingsManager:setOptionArgDict:Datatype missmatch: '+ section + '#' + setting + '=' +  value + ' Error:' +  str(e))
            #self.env['runtime']['debug'].writeDebugOut('settingsManager:setOptionArgDict:Datatype missmatch: '+ section + '#' + setting + '=' +  value + ' Error:' +  str(e), debug.debugLevel.ERROR)
            return



    def parseSettingArgs(self, settingArgs):
        for optionElem in settingArgs.split(';'):
            if len(optionElem.split('#',1)) != 2:
                continue
            if len(optionElem.split('#',1)[1].split('=',1)) != 2:
                continue

            section = str(optionElem.split('#',1)[0])
            option = str(optionElem.split('#',1)[1].split('=',1)[0])
            value = optionElem.split('#',1)[1].split('=',1)[1]
            self.setOptionArgDict(section, option, value)

    def initFenrirConfig(self, cliArgs, fenrirManager = None, environment = environment.environment):
        settingsRoot = '/etc/fenrirscreenreader/'
        settingsFile = cliArgs.setting
        soundRoot = '/usr/share/sounds/fenrirscreenreader/'
        # get fenrir settings root
        if not os.path.exists(settingsRoot):
            if os.path.exists(fenrirPath +'/../../config/'):
                settingsRoot = fenrirPath +'/../../config/'
            else:
                return None
        # get settings file
        if not os.path.exists(settingsFile):
            if os.path.exists(settingsRoot + '/settings/settings.conf'):
                settingsFile = settingsRoot + '/settings/settings.conf'
            else:
                return None
        # get sound themes root
        if not os.path.exists(soundRoot):
            if os.path.exists(fenrirPath + '/../../config/sound/'):
                soundRoot = fenrirPath + '/../../config/sound/'

        environment['runtime']['settingsManager'] = self 
        environment['runtime']['settingsManager'].initialize(environment)

        validConfig = environment['runtime']['settingsManager'].loadSettings(settingsFile)
        if not validConfig:
            return None
        if cliArgs.options != '':
            self.parseSettingArgs(cliArgs.options)
        if cliArgs.debug:
            self.setSetting('general', 'debugLevel', 3)
        if cliArgs.print:
            self.setSetting('general', 'debugLevel', 3)
            self.setSetting('general', 'debugMode', 'PRINT')
        if cliArgs.emulated_pty:
            self.setSetting('screen', 'driver', 'ptyDriver')
            self.setSetting('keyboard', 'driver', 'ptyDriver')
            # TODO needs cleanup use dict
            #self.setOptionArgDict('keyboard', 'keyboardLayout', 'pty')
            self.setSetting('keyboard', 'keyboardLayout', 'pty')
            self.setSetting('general', 'debugFile', '/tmp/fenrir-pty.log')
        if cliArgs.emulated_evdev:
            self.setSetting('screen', 'driver', 'ptyDriver')
            self.setSetting('keyboard', 'driver', 'evdevDriver')

        self.setFenrirKeys(self.getSetting('general','fenrirKeys'))
        self.setScriptKeys(self.getSetting('general','scriptKeys'))

        environment['runtime']['debug'] = debugManager.debugManager(self.env['runtime']['settingsManager'].getSetting('general','debugFile'))
        environment['runtime']['debug'].initialize(environment)

        if not os.path.exists(self.getSetting('sound','theme') + '/soundicons.conf'):
            if os.path.exists(soundRoot + self.getSetting('sound','theme')):
                self.setSetting('sound', 'theme', soundRoot + self.getSetting('sound','theme'))
                if os.path.exists(self.getSetting('sound','theme') + '/soundicons.conf'):
                    environment['runtime']['settingsManager'].loadSoundIcons(self.getSetting('sound','theme'))
        else:
            environment['runtime']['settingsManager'].loadSoundIcons(self.getSetting('sound','theme'))

        environment['runtime']['punctuationManager'] = punctuationManager.punctuationManager()
        environment['runtime']['punctuationManager'].initialize(environment) 

        environment['runtime']['textManager'] = textManager.textManager()
        environment['runtime']['textManager'].initialize(environment)

        if not os.path.exists(self.getSetting('general','punctuationProfile')):
            if os.path.exists(settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile')):  
                self.setSetting('general', 'punctuationProfile', settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile'))
                environment['runtime']['punctuationManager'].loadDicts(self.getSetting('general','punctuationProfile'))
            if os.path.exists(settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile') + '.conf'):  
                self.setSetting('general', 'punctuationProfile', settingsRoot + 'punctuation/' + self.getSetting('general','punctuationProfile') + '.conf')
                environment['runtime']['punctuationManager'].loadDicts(self.getSetting('general','punctuationProfile'))
        else:
            environment['runtime']['punctuationManager'].loadDicts(self.getSetting('general','punctuationProfile'))


        if fenrirManager:
            environment['runtime']['fenrirManager'] = fenrirManager

        environment['runtime']['memoryManager'] = memoryManager.memoryManager()
        environment['runtime']['memoryManager'].initialize(environment) 

        environment['runtime']['attributeManager'] = attributeManager.attributeManager()
        environment['runtime']['attributeManager'].initialize(environment)

        environment['runtime']['eventManager'] = eventManager.eventManager()
        environment['runtime']['eventManager'].initialize(environment)

        environment['runtime']['processManager'] = processManager.processManager()  
        environment['runtime']['processManager'].initialize(environment)

        environment['runtime']['outputManager'] = outputManager.outputManager()
        environment['runtime']['outputManager'].initialize(environment)

        environment['runtime']['byteManager'] = byteManager.byteManager()
        environment['runtime']['byteManager'].initialize(environment)

        environment['runtime']['inputManager'] = inputManager.inputManager()
        environment['runtime']['inputManager'].initialize(environment)

        environment['runtime']['screenManager'] = screenManager.screenManager()
        environment['runtime']['screenManager'].initialize(environment)

        environment['runtime']['commandManager'] = commandManager.commandManager()
        environment['runtime']['commandManager'].initialize(environment)

        environment['runtime']['helpManager'] = helpManager.helpManager()
        environment['runtime']['helpManager'].initialize(environment)

        environment['runtime']['remoteManager'] = remoteManager.remoteManager()
        environment['runtime']['remoteManager'].initialize(environment)


        if environment['runtime']['inputManager'].getShortcutType() == 'KEY':
            if not os.path.exists(self.getSetting('keyboard','keyboardLayout')):
                if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout')):  
                    self.setSetting('keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout'))
                    environment['runtime']['inputManager'].loadShortcuts(self.getSetting('keyboard','keyboardLayout'))
                if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout') + '.conf'):  
                    self.setSetting('keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout') + '.conf')
                    environment['runtime']['inputManager'].loadShortcuts(self.getSetting('keyboard','keyboardLayout'))
            else:
                environment['runtime']['inputManager'].loadShortcuts(self.getSetting('keyboard','keyboardLayout'))
        elif environment['runtime']['inputManager'].getShortcutType() == 'BYTE':
            if not os.path.exists(self.getSetting('keyboard','keyboardLayout')):
                if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout')):  
                    self.setSetting('keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout'))
                    environment['runtime']['byteManager'].loadByteShortcuts(self.getSetting('keyboard','keyboardLayout'))
                if os.path.exists(settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout') + '.conf'):  
                    self.setSetting('keyboard', 'keyboardLayout', settingsRoot + 'keyboard/' + self.getSetting('keyboard','keyboardLayout') + '.conf')
                    environment['runtime']['byteManager'].loadByteShortcuts(self.getSetting('keyboard','keyboardLayout'))
            else:
                environment['runtime']['byteManager'].loadByteShortcuts(self.getSetting('keyboard','keyboardLayout'))

        environment['runtime']['cursorManager'] = cursorManager.cursorManager()
        environment['runtime']['cursorManager'].initialize(environment)
        environment['runtime']['applicationManager'] = applicationManager.applicationManager()
        environment['runtime']['applicationManager'].initialize(environment)
        environment['runtime']['textManager'] = textManager.textManager()
        environment['runtime']['textManager'].initialize(environment)
        environment['runtime']['tableManager'] = tableManager.tableManager()
        environment['runtime']['tableManager'].initialize(environment)
        environment['runtime']['barrierManager'] = barrierManager.barrierManager()
        environment['runtime']['barrierManager'].initialize(environment)
        environment['runtime']['sayAllManager'] = sayAllManager.sayAllManager()
        environment['runtime']['sayAllManager'].initialize(environment)
        environment['runtime']['vmenuManager'] = vmenuManager.vmenuManager()
        environment['runtime']['vmenuManager'].initialize(environment)
        environment['runtime']['quickMenuManager'] = quickMenuManager.quickMenuManager()
        environment['runtime']['quickMenuManager'].initialize(environment)
        environment['runtime']['debug'].writeDebugOut('\/-------environment-------\/',debug.debugLevel.INFO, onAnyLevel=True)
        environment['runtime']['debug'].writeDebugOut(str(environment), debug.debugLevel.INFO, onAnyLevel=True)
        environment['runtime']['debug'].writeDebugOut('\/-------settings.conf-------\/', debug.debugLevel.INFO, onAnyLevel=True)
        environment['runtime']['debug'].writeDebugOut(str(environment['settings']._sections) , debug.debugLevel.INFO, onAnyLevel=True)
        environment['runtime']['debug'].writeDebugOut('\/-------self.settingArgDict-------\/',debug.debugLevel.INFO, onAnyLevel=True)
        environment['runtime']['debug'].writeDebugOut(str( self.settingArgDict) ,debug.debugLevel.INFO, onAnyLevel=True)
        self.bindingsBackup = environment['bindings'].copy()

        return environment

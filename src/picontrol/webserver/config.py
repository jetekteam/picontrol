#!/usr/bin/python 
#config.py

import sys, ConfigParser

basePath = '/home/pi/scripts/picontrol/configs'
updatePath = '/home/pi/scripts/picontrol_update/picontrol/configs'

class Config():
    @staticmethod
    def loadConfig():
        config = ConfigParser.RawConfigParser()
        configFilePath = basePath + '/config.conf'
        config.read(configFilePath)
        return config
    
    @staticmethod
    def saveConfig(config):
        with open(basePath + '/config.conf', 'w') as configFile:
            config.write(configFile)
        return True

    @staticmethod
    def loadVersion():
        config = ConfigParser.RawConfigParser()
        configFilePath = basePath + '/picontrol.version'
        config.read(configFilePath)
        return config
    
    @staticmethod
    def saveVersion(config):
        with open(basePath + '/picontrol.version', 'w') as configFile:
            config.write(configFile)
        return True

    @staticmethod
    def loadUpdateVersion():
        config = ConfigParser.RawConfigParser()
        configFilePath = updatePath + '/picontrol.version'
        config.read(configFilePath)
        return config
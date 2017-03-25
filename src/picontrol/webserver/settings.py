#!/usr/bin/python 
#settings.py

import sys, os
from config import Config

updateDir = '/home/pi/scripts/picontrol_update'
baseDir = '/home/pi/scripts/picontrol'

class Settings():
    @staticmethod
    def setFanSettings(fanSettings):
        try:
            config = Config.loadConfig()
            config.set("fan", "thresholdOn", fanSettings['thresholdOn'])   
            config.set("fan", "thresholdOff", fanSettings['thresholdOff'])
            config.set("fan", "interval", fanSettings['interval'])

            Config.saveConfig(config)
            return True
        except:
            return False

    @staticmethod
    def getFanSettings():
        try:
            config = Config.loadConfig()
            thresholdOn = int(config.get("fan", "thresholdOn"))  
            thresholdOff = int(config.get("fan", "thresholdOff"))  
            interval = int(config.get("fan", "interval"))             

            return {"thresholdOn":thresholdOn, "thresholdOff":thresholdOff, "interval":interval}
        except:
            return {"thresholdOn":0, "thresholdOff":0, "interval":0}

    @staticmethod
    def setButtonSettings(option):
        try:
            config = Config.loadConfig()
            config.set("button", "option", option["option"])
            
            Config.saveConfig(config)
            return True
        except:
            return False

    @staticmethod
    def getButtonSettings():
        try:
            config = Config.loadConfig()
            option = int(config.get("button", "option"))

            return {"option":option}
        except:
            return {"option":0}

    @staticmethod
    def getVersion():
        try:
            config = Config.loadVersion()
           
            number = config.get("version", "number")
            date = config.get("version", "date")

            return {'number':number, 'date':date}
        except:
            return {'number':'1.0', 'date':''}

    @staticmethod
    def getUpdateVersion():
        try:
            config = Config.loadUpdateVersion()
           
            number = config.get("version", "number")
            date = config.get("version", "date")

            return {'number':number, 'date':date}
        except:
            return {'number':'1.0', 'date':''}

    @staticmethod
    def checkUpdates():
        response = {"update":False}
        try:            
            currentVersion = Settings.getVersion()
            
            os.system('mkdir ' + updateDir)
            os.system('wget --no-check-certificate --content-disposition https://github.com/jetechteam/picontrol/raw/master/picontrol.tgz')
            os.system('tar -xzf picontrol.tgz picontrol')
            os.system('mv ./picontrol ' + updateDir + '/picontrol')

            updateVersion = Settings.getUpdateVersion()

            if currentVersion['number'] != updateVersion['number']:
                response =  {"update":True}

            os.system("sudo rm -R " + updateDir)            
            os.system("sudo rm -R picontrol picontrol.tgz") 
        except:
            os.system("sudo rm -R " + updateDir) 
            os.system("sudo rm -R picontrol picontrol.tgz") 
            response = {"update":False}
        
        return response

    @staticmethod
    def updateVersion():
        response = {"update":False}
        try:                        
            os.system('mkdir ' + updateDir)
            os.system('wget --no-check-certificate --content-disposition https://github.com/jetechteam/picontrol/raw/master/picontrol.tgz')
            os.system('tar -xzf picontrol.tgz picontrol')
            os.system('mv ./picontrol ' + updateDir + '/picontrol')
            os.system('cp ' + baseDir + '/configs/config.conf ' + updateDir + '/picontrol/configs/config.conf')
            print('copied config')
            os.system('sudo rm -R ' + baseDir)
            print('deleted base')
            os.system('cp -R ' + updateDir + '/picontrol ' + baseDir)
            print('copied update')

            os.system("sudo rm -R " + updateDir)            
            os.system("sudo rm -R picontrol picontrol.tgz")
            response = {"update":Settings.getVersion()["number"]}
        except:
            print('error')
            os.system("sudo rm -R " + updateDir) 
            os.system("sudo rm -R picontrol picontrol.tgz") 
            response = {"update":False}
        
        return response

import sys, os
import re
import picontrol.config
import packaging.version
import subprocess


class Settings():
    @staticmethod
    def setFanSettings(fanSettings):
        try:
            config = picontrol.config.load_config()
            config.set("fan", "thresholdOn", fanSettings['thresholdOn'])
            config.set("fan", "thresholdOff", fanSettings['thresholdOff'])
            config.set("fan", "interval", fanSettings['interval'])

            picontrol.config.save_config(config)
            return True
        except:
            return False

    @staticmethod
    def getFanSettings():
        try:
            config = picontrol.config.load_config()
            thresholdOn = int(config.get("fan", "thresholdOn"))
            thresholdOff = int(config.get("fan", "thresholdOff"))
            interval = int(config.get("fan", "interval"))

            return {"thresholdOn":thresholdOn, "thresholdOff":thresholdOff, "interval":interval}
        except:
            return {"thresholdOn":0, "thresholdOff":0, "interval":0}

    @staticmethod
    def setButtonSettings(option):
        try:
            config = picontrol.config.load_config()
            config.set("button", "option", option["option"])

            picontrol.config.save_config(config)
            return True
        except:
            return False

    @staticmethod
    def getButtonSettings():
        try:
            config = picontrol.config.load_config()
            option = int(config.get("button", "option"))

            return {"option":option}
        except:
            return {"option":0}

    @staticmethod
    def getVersion():
        version_re = r"^Version: (?P<version>\d+\.\d+\.\d+).*?$"
        try:
            result = subprocess.check_output('pip show picontrol')
            match = re.match(version_re, result, re.MULTILINE)
            version = match.group('version')
            return {'number':version, 'date':''}
        except subprocess.CalledProcessError, AttributeError:
            return {'number':'1.0', 'date':''}

    @staticmethod
    def getUpdateVersion():
        version_re = r"^picontrol (?P<version>\d+\.\d+\.\d+) .*?$"
        try:
            result = subprocess.check_output('pip search picontrol')
            match = re.match(version_re, result, re.MULTILINE)
            version = match.group('version')
            return {'number':version, 'date':''}
        except subprocess.CalledProcessError, AttributeError:
            return {'number':'1.0', 'date':''}

    @staticmethod
    def checkUpdates():
        current_version = packaging.version.parse(Settings.getVersion()['number'])
        update_version = packaging.version.parse(Settings.getUpdateVersion()['number'])
        if current_version < update_version:
            return {"update":True}
        return {"update":False}

    @staticmethod
    def updateVersion():
        try:
            result = subprocess.check_output('pip install -U picontrol')
            return {"update":Settings.getVersion()["number"]}
        except subprocess.CalledProcessError:
            return {"update":False}

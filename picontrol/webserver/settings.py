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
        version_re = r"^Version: (?P<version>\d+\.\d+(\.\d+)?).*?$"
        try:
            result = subprocess.check_output('pip show picontrol', shell=True)
            match = re.search(version_re, result, re.MULTILINE)
            version = match.group('version')
            return {'number':version, 'date':''}
        except (subprocess.CalledProcessError, AttributeError):
            return {'number':'1.0', 'date':''}

    @staticmethod
    def checkUpdates():
        exitcode = subprocess.call('pip list -o --format=columns| grep picontrol', shell=True)
        if exitcode == 0:
            return {"update":True}
        return {"update":False}

    @staticmethod
    def updateVersion():
        try:
            subprocess.check_output('sudo pip install -U picontrol', shell=True)
            return {"update":Settings.getVersion()["number"]}
        except subprocess.CalledProcessError:
            return {"update":False}

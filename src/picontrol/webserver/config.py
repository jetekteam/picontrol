import sys, ConfigParser
import picontrol
import os

CONFIG_PATHS = ["~/.picontrol", "~/scripts/picontrol/configs"]
UPDATE_PATHS = ["~/.picontrol_update", "~/scripts/picontrol_update/picontrol/configs"]

class Config():
    @staticmethod
    def loadConfig():
        config = ConfigParser.RawConfigParser()
        config.read([os.join(path, 'config.conf') for path in CONFIG_PATHS])
        return config

    @staticmethod
    def saveConfig(config):
        with open(os.join(CONFIG_PATHS[0], 'config.conf'), 'w') as configFile:
            config.write(configFile)

    @staticmethod
    def loadVersion():
        config = ConfigParser.RawConfigParser()
        config.read([os.join(path, 'picontrol.version') for path in CONFIG_PATHS])
        return config

    @staticmethod
    def loadUpdateVersion():
        config = ConfigParser.RawConfigParser()
        config.read([os.join(path, 'picontrol.version') for path in UPDATE_PATHS])
        return config

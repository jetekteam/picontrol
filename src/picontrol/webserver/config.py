import sys, ConfigParser
import picontrol
import os

CONFIG_PATHS = ["~/.picontrol", "~/scripts/picontrol/configs"]

class Config():
    @staticmethod
    def loadConfig():
        config = ConfigParser.RawConfigParser()
        config.read([os.path.join(path, 'config.conf') for path in CONFIG_PATHS])
        return config

    @staticmethod
    def saveConfig(config):
        with open(os.path.join(CONFIG_PATHS[0], 'config.conf'), 'w') as configFile:
            config.write(configFile)

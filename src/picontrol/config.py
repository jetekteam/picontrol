import ConfigParser
import os

CONFIG_PATHS = ["~/.picontrol", "~/scripts/picontrol/configs"]

def load_config():
    config = ConfigParser.RawConfigParser()
    config.read([os.path.join(path, 'config.conf') for path in CONFIG_PATHS])
    return config

def save_config(config):
    with open(os.path.join(CONFIG_PATHS[0], 'config.conf'), 'w') as configFile:
        config.write(configFile)

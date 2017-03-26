import ConfigParser
import os

CONFIG_PATHS = [
    "/etc/picontrol/picontrol.conf",
    "~/.picontrol/picontrol.conf",
    "~/scripts/picontrol/configs/config.conf",
]

def load_config():
    config = ConfigParser.RawConfigParser()
    config.read(CONFIG_PATHS)
    return config

def save_config(config):
    try:
        os.makedirs(os.path.split(CONFIG_PATHS[0]))
    except OSError as e:
        if not "File exists" in str(e):
            raise

    with open(CONFIG_PATHS[0], 'w') as configFile:
        config.write(configFile)
    os.chmod(CONFIG_PATHS[0], 438) #ensure permissions

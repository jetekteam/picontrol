import ConfigParser
import os
import StringIO

CONFIG_PATHS = [
    "/etc/picontrol/picontrol.conf",
    "~/.picontrol/picontrol.conf",
    "~/scripts/picontrol/configs/config.conf",
]

DEFAULTS = """
[user]
username = picontrol
password = password
theme = default

[fan]
thresholdon = 60
thresholdoff = 40
interval = 10

[button]
option = 1
"""

def load_config():
    config = ConfigParser.RawConfigParser()
    config.readfp(StringIO.StringIO(DEFAULTS))
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

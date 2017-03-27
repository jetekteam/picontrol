import contextlib
import os
import re
import subprocess

from setuptools import setup
from setuptools.command.sdist import sdist

DATA_ROOTS = [
    "picontrol/webserver/templates",
    "picontrol/webserver/static",
]
PROJECT = 'picontrol'
VERSION_FILE = 'picontrol/__init__.py'

def _get_output_or_none(args):
    try:
        return subprocess.check_output(args).decode('utf-8').strip()
    except subprocess.CalledProcessError:
        return None

def _get_git_description():
    return _get_output_or_none(['git', 'describe'])

def _get_git_branches_for_this_commit():
    branches = _get_output_or_none(['git', 'branch', '-r', '--contains', 'HEAD'])
    split = branches.split('\n') if branches else []
    return [branch.strip() for branch in split]

def _git_to_version(git):
    match = re.match(r'(?P<tag>[\d\.]+)-(?P<offset>[\d]+)-(?P<sha>\w{8})', git)
    if not match:
        version = git
    else:
        version = "{tag}.post0.dev{offset}".format(**match.groupdict())
    return version

def _get_version_from_git():
    git_description = _get_git_description()
    git_branches = _get_git_branches_for_this_commit()
    version = _git_to_version(git_description) if git_description else None
    return version

def get_version():
    git_version = _get_version_from_git()
    return git_version

def get_data_files():
    data_files = []
    for data_root in DATA_ROOTS:
        for root, _, files in os.walk(data_root):
            data_files.append((os.path.join(PROJECT, root), [os.path.join(root, f) for f in files]))
    return data_files

def main():
    setup(
        name                = "picontrol",
        version             = get_version(),
        description         = "A RaspberryPi/RetroPi controller/webserver for game, nfc, and power control",
        url                 = "https://github.com/Lemmons/picontrol",
        long_description    = "A RaspberryPi/RetroPi controller/webserver for game, nfc, and power control",
        author              = "Scott Lemmon",
        install_requires    = [
            "Adafruit_PN532",
            "RPi.GPIO==0.6.3",
            "flask-api==0.6.9",
            "flask-httpauth==3.2.2",
            "flask==0.12",
            "psutil==5.2.1",
        ],
        dependency_links=[
            "git+https://github.com/adafruit/Adafruit_Python_PN532.git",
        ],
        extras_require      = { },
        packages            = [
            "picontrol",
            "picontrol.webserver",
        ],
        package_data         = {
            "picontrol"        : ["picontrol/*"],
            "picontrol.webserver" : ["picontrol/webserver/*"],
        },
        data_files           = get_data_files(),
        entry_points={
            'console_scripts': [
                'picontrol          = picontrol.picontrol:main',
                'pic_button_classic = picontrol.button_classic:main',
                'pic_button_pi      = picontrol.button_pi:main',
                'pic_fan            = picontrol.fan:main',
                'pic_gameend        = picontrol.gameend:main',
                'pic_gamestart      = picontrol.gamestart:main',
                'pic_web            = picontrol.webserver.picontrol_web:main',
            ]
        },
        include_package_data= True,
    )

if __name__ == "__main__":
    main()

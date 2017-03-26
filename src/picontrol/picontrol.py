#!/usr/bin/env python
import sys, os, time, json, subprocess, ConfigParser
import RPi.GPIO as GPIO
from picontrol import processes as procs
from picontrol import nfc

CONFIG_PATHS = ["~/.picontrol", "~/scripts/picontrol/configs"]

def getConfig():
    config = ConfigParser.RawConfigParser()
    config.read([os.path.join(path, 'config.conf') for path in CONFIG_PATHS])
    return config

#start fan
os.system('pkill -9 -f fan.py')
subprocess.Popen('fan.py&', shell=True)

#start webserver
os.system('pkill -9 -f picontrol_web.py')
os.system('sudo iptables -A PREROUTING -t nat -p tcp --dport 80 -j REDIRECT --to-port 8080')
subprocess.Popen('picontrol_web.py&', shell=True)

#get button option and start the process
os.system('pkill -9 -f button_pi.py')
os.system('pkill -9 -f button_classic.py')
config = getConfig()
buttonOption = int(config.get("button", "option"))

if buttonOption == 1:
    subprocess.Popen('python button_classic.py&', shell=True)
else:
    subprocess.Popen('python button_pi.py&', shell=True)

#check if we have a tag inserted and boot that game
response = nfc.read()

if response.type == 'success':
    message = response.data
    procs.runGame(message.records[0].value, message.records[1].value, 'nfc')
